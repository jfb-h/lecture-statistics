from fasthtml.common import *
import json
import dataclasses
import polars as pl
from components import Survey, Items, QRCode, PlotContainer, StyledGrid, StyledCard, Choice, Radio, NumericInput


def choice_datatype(name, title):
    return Choice(
        Radio(name, "num-kon", "numerisch (kontinuierlich)"), 
        Radio(name, "num-dis", "numerisch (diskret)"), 
        Radio(name, "kat-nom", "kategorisch (nominal)"), 
        Radio(name, "kat-nom", "kategorisch (ordinal)"), 
        title=title
    )

# SURVEY DATATYPES

def init_datatypes(db, rt, route, tablename, **kwargs):
    table = db.t[tablename]
    if table not in db.t:
        table.create(id=int, pk="id", **kwargs)

    Item = table.dataclass()

    # SURVEY FORM AND POST SPEC

    @rt(f"/{route}")
    def get():
        question = H4("Was ist der Datentyp der folgenden Variablen?")

        i1 = choice_datatype("bip", "Das deutsche BIP")
        i2 = choice_datatype("co2", "Die CO₂-Konzentration in der Atmosphäre")
        i3 = choice_datatype("stars", "Sterne zur Produktbewertung bei Amazon")
        i4 = choice_datatype("likes", "Likes eines Youtube-Videos")
        i5 = choice_datatype("shf", "Der Anteil weiblicher Studierender")
        i6 = choice_datatype("gen", "Generationszugehörigkeit (Boomer, Millienials, Gen Z, ...)")

        items = Items(question, i1, i2, i3, i4, i5, i6, hx_post=f"/statlecture/{route}")
        return Survey("Datentypen", items)

    @rt(f"/{route}")
    def post(item: Item):
        table.insert(item)
        return Strong("Danke für deine Antwort!")

    @rt(f"/{route}/qr")
    def get(): return QRCode(f"{route}")

    @rt(f"/{route}/data")
    async def get():
        df = pl.read_database("SELECT * FROM datentypen", db)
        rows = df.unpivot(index='id').write_json()
        return rows

    update_data = ScriptX("session-01/fetch-data.js")
    obs_results = ScriptX("session-02/obs-datatypes.js", type="module")

    @rt(f"/{route}/results")
    async def get():
        plot = StyledCard(
            PlotContainer(id="results"),
            header=H2("Welche Datenniveaus haben diese Variablen?"),
        )
        grid = StyledGrid(plot)
        return Title("Einführung"), Main(grid, update_data, obs_results, cls="container")


# SURVEY LIVINGCOST

def init_livingcost(db, rt, route, tablename, **kwargs):
    table = db.t[tablename]
    if table not in db.t:
        table.create(id=int, pk="id", **kwargs)

    Item = table.dataclass()

    @rt(f"/{route}")
    def get():
        num = NumericInput("kosten", "Wie viel gibst du montlich für's Wohnen aus?", "0", "10000")

        choice = Choice(
            Radio("wohnsituation", "Familie", "Ich wohne bei meinen Eltern / meiner Familie"),
            Radio("wohnsituation", "Alleine", "Ich wohne alleine"),
            Radio("wohnsituation", "WG", "Ich wohne in einer WG"),
            Radio("wohnsituation", "Andere", "Andere"),
            title="Was trifft auf deine Wohnsituation zu?",
        )

        return Survey( "Kurzumfrage", Items(num, choice, hx_post=f"/statlecture/{route}"))

    @rt(f"/{route}")
    def post(item: Item):
        table.insert(item)
        return Strong("Danke für deine Antwort!")

    @rt(f"/{route}/qr")
    def get(): return QRCode(f"{route}")

    @rt(f"/{route}/data")
    async def get():
        return json.dumps([dataclasses.asdict(item) for item in table()], ensure_ascii=False)

    update_data = ScriptX("session-01/fetch-data.js")
    obs_results = ScriptX("session-02/obs-livingcost.js", type="module")

    @rt(f"/{route}/results")
    async def get():
        plot = StyledCard(
            PlotContainer(id="wohnsituation")
        )

        c1 = Card(Div(id="c1"), header=Strong("Alleine"), style="height: 200px")
        c2 = Card(Div(id="c2"), header=Strong("Familie"), style="height: 200px")
        c3 = Card(Div(id="c3"), header=Strong("WG"), style="height: 200px")

        grid = Grid(Div(c1, c2, c3), plot,
            style = f"grid-template-columns: 1fr 4fr; grid-template-rows: none; height: 90vh;"
        )
        

        return Title("Einführung"), Main(H2("Wie viel geben Studierende in München für das Wohnen aus?"), grid, update_data, obs_results, cls="container")


# SERVER AND DB INITIALIZATION 

db = database("surveys.db")
app, rt = fast_app(live=True)

init_datatypes(
    db, rt, "datentypen", "datentypen",
    bip=str, co2=str, stars=str, likes=str, shf=str, gen=str
)

init_livingcost(
    db, rt, "wohnsituation", "wohnsituation",
    kosten=float, wohnsituation=str
)

serve(port=8081)
