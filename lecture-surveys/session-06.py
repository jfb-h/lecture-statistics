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


def init_sizes(db, rt, route, tablename, **kwargs):
    # DATABASE SETUP

    table = db.t[tablename]
    if table not in db.t:
        table.create(id=int, pk="id", **kwargs)

    Item = table.dataclass()

    # SURVEY FORM AND POST SPEC

    @rt(f"/{route}")
    def get():
        va = NumericInput("vara", "Wie groß bist du (z.B. 180 cm)?", min=100, max=250)
        vb = NumericInput("varb", "Was ist deine Schuhgröße (z.B. 43)?", min=30, max=60)
        
        items = Items(va, vb, hx_post=f"/statlecture/{route}")
        return Survey("Kurzumfrage", items)
        

    @rt(f"/{route}")
    def post(item: Item):
        table.insert(item)
        return Strong("Danke für deine Antwort!")

    @rt(f"/{route}/data")
    async def get():
        return json.dumps([dataclasses.asdict(item) for item in table()], ensure_ascii=False)

    @rt(f"/{route}/qr")
    def get():
        return QRCode(f"{route}")

    # RESULT PLOTS

    update_data = ScriptX("session-01/fetch-data.js")

    observable_scatter = ScriptX("session-06/obs-scatter-cor.js", type="module")

    @rt(f"/{route}/result")
    async def get():
        scatter = StyledCard(
            PlotContainer(id="scatter"),
            header=H2("Körpergröße vs. Schuhgröße")
        )
        c1 = Card(Div(id="c1"), header=Strong("Mittelwert"))
        c2 = Card(Div(id="c2"), header=Strong("Kovarianz"))
        c3 = Card(Div(id="c3"), header=Strong("Korrelation"))

        grid = Grid(
            Div(c1, c2, c3), scatter,
            style = f"grid-template-columns: 1fr 4fr; grid-template-rows: none; height: 90vh;"
        )
        return Title("Ergebnis"), Main(grid, update_data, observable_scatter, cls="container")



def init_news(db, rt, route, tablename, **kwargs):
    # DATABASE SETUP

    table = db.t[tablename]
    if table not in db.t:
        table.create(id=int, pk="id", **kwargs)

    Item = table.dataclass()

    # SURVEY FORM AND POST SPEC

    @rt(f"/{route}")
    def get():
        choicemedia = Choice(
            Radio("media","Soc. Media", "Social Media (z.B. Instagram, TikTok, Facebook)"),
            Radio("media","Zeitung DE", "Deutschsprachige Zeitungen (z.B. FAZ, Zeit, Sueddeutsche, TAZ, NZZ)",),
            Radio("media","Zeitung Int", "Internationale Zeitungen (z.B. Guardian, NYT, Economist, LeMonde)",),
            Radio("media","TV / Radio", "TV oder Radio"),
            Radio("media","Sonstige", "Sonstige"),
            title="Welche Quellen nutzt du primär, um dich über aktuelle Ereignisse zu informieren?",
        )

        choiced = Choice(
            Radio("wahl_d", "Union", "CSU/CDU"),
            Radio("wahl_d", "SPD", "SPD"),
            Radio("wahl_d", "Gruene", "Grüne"),
            Radio("wahl_d", "FDP", "FDP"),
            Radio("wahl_d", "AfD", "AfD"),
            Radio("wahl_d", "Sonstige", "Sonstige"),
            title="Sonntagsfrage: Welche Partei würdest du wählen, wenn nächsten Sonntag Bundestagswahl wäre?",
        )

        items = Items(choicemedia, choiced, hx_post=f"/statlecture/{route}")
        return Survey("Kurzumfrage", items)
        

    @rt(f"/{route}")
    def post(item: Item):
        table.insert(item)
        return Strong("Danke für deine Antwort!")

    @rt(f"/{route}/data")
    async def get():
        return json.dumps([dataclasses.asdict(item) for item in table()], ensure_ascii=False)

    @rt(f"/{route}/qr")
    def get():
        return QRCode(f"{route}")

    # RESULT PLOTS

    update_data = ScriptX("session-01/fetch-data.js")
    observable_wahlen = ScriptX("session-06/obs-wahlen-kont.js", type="module")

    @rt(f"/{route}/result")
    async def get():
        wahlen = StyledCard(
            Grid(
                PlotContainer(id="wahlen"),
                PlotContainer(id="wahlen_heat"),
                style = f"grid-template-columns: 1fr 1fr; grid-template-rows: none; height: 100%;"
            ),
            header=H2("Ergebnis"),
        )
        c4 = Card(Div(id="c4"), header=Strong("Chi-Quadrat"))
        c5 = Card(Div(id="c5"), header=Strong("Kontingenzkoeffizient"))
        grid = Grid(Div(c4, c5), wahlen,
            style = f"grid-template-columns: 1fr 4fr; grid-template-rows: none; height: 90vh;"
        )
        return Title("Einführung"), Main(grid, update_data, observable_wahlen, cls="container")


# SERVER AND DB INITIALIZATION 

db = database("surveys.db")

app, rt = fast_app(live=True, hdrs=(leaflet_css, leaflet_js, pico_leaflet))
init_sizes(db, rt, "bodysize", "bodysize", vara=float, varb=float)
init_news(db, rt, "news", "news", media=str, wahl_d=str)

serve(port=8081)
