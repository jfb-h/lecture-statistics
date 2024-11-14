from fasthtml.common import *  # Link, Script, StyleX, ScriptX, Option,
import pgeocode
import json
import dataclasses
import polars as pl
from helpers import simulate_latlon
from components import Survey, Items, QRCode, TextInput, TimeInput, NumericInput, SelectInput, PlotContainer, StyledGrid, StyledCard, Choice, Radio


leaflet_css = Link(rel="stylesheet", href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css")
leaflet_js = Script(src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js")

pico_leaflet = StyleX("session-01/pico-leaflet.css")
update_data = ScriptX("session-01/fetch-data.js")


def init_app(db, rt, route, tablename, **kwargs):
    # DATABASE SETUP

    table = db.t[tablename]
    if table not in db.t:
        table.create(id=int, pk="id", **kwargs)

    Item = table.dataclass()

    # SURVEY FORM AND POST SPEC

    @rt(f"/{route}")
    def get():
        va = NumericInput("vara", "Variable A?", min=0, max=100)
        vb = NumericInput("varb", "Variable B", min=0, max=100)
        
        choiceus = Choice(
            Radio("wahl_us", "harris", "Kamala Harris"),
            Radio("wahl_us", "trump", "Donald Trump"),
            title="Wen hättest du in den USA gewählt?",
        )

        choiced = Choice(
            Radio("wahl_d", "union", "CSU/CDU"),
            Radio("wahl_d", "spd", "SPD"),
            Radio("wahl_d", "gr", "Grüne"),
            Radio("wahl_d", "fdp", "FDP"),
            Radio("wahl_d", "afd", "AfD"),
            Radio("wahl_d", "sonstige", "Sonstige"),
            title="Wen würdest du in D wählen?",
        )

        items = Items(va, vb, choiceus, choiced, hx_post=f"/{route}")
        return Survey("Kurzumfrage", items)
        

    @rt(f"/{route}")
    def post(item: Item):
        table.insert(item)
        return Strong("Danke für deine Antwort!")

    """
    @rt(f"/{route}/data")
    async def get():
    # Step 1: Read the database and unpivot the table
        df = pl.read_database("SELECT * FROM correlation", db).unpivot(index='id')
    
        # Step 2: Apply transformations only to columns that are not 'vara' or 'varb'
        df = df.with_columns(
            pl.when(~pl.col("variable").is_in(["vara", "varb"]))
            .then(pl.col("variable").str.split("_"))
            .otherwise(pl.col("variable").map_elements(lambda x: [x]))
            .alias("split_variable")
        )
    
    # Step 3: Extract components from 'split_variable' only for transformed columns
        df = (
            df.with_columns([
                pl.when(~pl.col("variable").is_in(["vara", "varb"]))
                .then(pl.col("split_variable").list.get(0))
                .otherwise(pl.lit(None))
                .alias("d"),

                pl.when(~pl.col("variable").is_in(["vara", "varb"]))
                .then(pl.col("split_variable").list.get(1))
                .otherwise(pl.lit(None))
                .alias("us")
            ])
            .drop("split_variable")
        )
        return df.write_json()
    """

    @rt(f"/{route}/simulate")
    async def get():
        global N_SIM
        N_SIM += 1
        if N_SIM > 300:
            return json.dumps([simulate_latlon() for i in range(300)])
        else:
            return json.dumps([simulate_latlon() for i in range(N_SIM)])

    @rt(f"/{route}/data")
    async def get():
        return json.dumps([dataclasses.asdict(item) for item in table()], ensure_ascii=False)

    @rt(f"/{route}/qr")
    def get():
        return QRCode(f"{route}")

    # RESULT PLOTS

    update_data = ScriptX("session-01/fetch-data.js")

    observable_scatter = ScriptX("session-06/obs-scatter-cor.js", type="module")

    @rt(f"/{route}/scatter")
    async def get():
        scatter = StyledCard(
            PlotContainer(id="scatter"),
            header=H2("Korrelation?"),
            footer=Div(
                Label(Input(type="checkbox", id="check-isoline"), "Isolinie", style="padding: 2px 10px"),
                Label(Input(type="checkbox", id="check-regression"), "Lineare Regression", style="padding: 2px 10px"),
                style="display: flex"
            )
        )
        c1 = Card(Div(id="c1"), header=Strong("Korrelationkoeffizient"))
        grid = Grid(c1, scatter,
            style = f"grid-template-columns: 1fr 4fr; grid-template-rows: none; height: 90vh;"
        )
        return Title("Einführung"), Main(grid, update_data, observable_scatter, cls="container")


    
    observable_wahlen = ScriptX("session-06/obs-wahlen-kont.js", type="module")

    @rt(f"/{route}/wahlen")
    async def get():
        wahlen = StyledCard(
            PlotContainer(id="wahlen"),
            header=H2("Ergebnis"),
        )
        c2 = Card(Div(id="c2"), header=Strong("Kontingenzkoeffizient"))
        grid = Grid(c2, wahlen,
            style = f"grid-template-columns: 1fr 4fr; grid-template-rows: none; height: 90vh;"
        )
        return Title("Einführung"), Main(grid, update_data, observable_wahlen, cls="container")
    


# SERVER AND DB INITIALIZATION 

route = "correlation"
table = "correlation"

db = database("surveys.db")

app, rt = fast_app(live=True, hdrs=(leaflet_css, leaflet_js, pico_leaflet))

init_app(db, rt, route, table, vara=float, varb=float, wahl_us=str, wahl_d=str)

serve(port=8081)
