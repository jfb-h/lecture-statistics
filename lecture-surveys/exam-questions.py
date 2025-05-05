from fasthtml.common import *
import json
import dataclasses
import polars as pl
from components import Survey, Items, QRCode, PlotContainer, StyledGrid, StyledCard, Choice, Radio, NumericInput

# überflutungsrisiko

def likert(name, title):
    return Choice(
        Radio(name, "1", "1 - gar nicht sicher"),
        Radio(name, "2", "2"),
        Radio(name, "3", "3"),
        Radio(name, "4", "4"),
        Radio(name, "5", "5 - sehr sicher"),
        title=title
    )

# SURVEY measures

def init_questions(db, rt, route, tablename, **kwargs):
    table = db.t[tablename]
    if table not in db.t:
        table.create(id=int, pk="id", **kwargs)

    Item = table.dataclass()

    # SURVEY FORM AND POST SPEC

    @rt(f"/{route}")
    def get():
        h = H4("Wie sicher fühlt ihr euch mit folgenden Themen?")

        q1 = likert("Datentypen", "Datentypen")
        q2 = likert("Visualisierung", "Visualisierung")
        q3 = likert("Lagemaße", "Lagemaße")
        q4 = likert("Streuungsmaße", "Streuungsmaße")
        q5 = likert("Zusammenhangsmaße", "Zusammenhangsmaße")
        q6 = likert("Autokorrelation", "Autokorrelation")
        q7 = likert("Modelle", "Statistische Modelle")
        q8 = likert("Wahrscheinlichkeit", "Wahrscheinlichkeitstheorie")

        items = Items(
            h, q1, q2, q3, q4, q5, q6, q7, q8,
            hx_post=f"/statlecture/{route}"
        )
        return Survey("Themen der Vorlesung", items)

    @rt(f"/{route}")
    def post(item: Item):
        table.insert(item)
        return Strong("Danke für deine Antwort!")

    @rt(f"/{route}/qr")
    def get(): return QRCode(f"{route}")

    @rt(f"/{route}/data")
    async def get():
        df = pl.read_database("SELECT * FROM examquestions", db).unpivot(index='id')
        return df.write_json()


    update_data = ScriptX("session-01/fetch-data.js")
    obs_results = ScriptX("session-11/obs-exam-questions.js", type="module")

    @rt(f"/{route}/results")
    async def get():
        plot = StyledCard(
            PlotContainer(id="results"),
            header=H2("Themen der Vorlesung"),
        )
        grid = StyledGrid(plot)
        return Title("Einführung"), Main(grid, update_data, obs_results, cls="container")


# SERVER AND DB INITIALIZATION

db = database("surveys.db")
app, rt = fast_app(live=True)

init_questions(
    db, rt, "examquestions", "examquestions",
    Visualisierung = str, Datentypen = str,
    Lagemaße = str, Streuungsmaße = str, Zusammenhangsmaße = str,
    Autokorrelation = str, Modelle = str, Wahrscheinlichkeit = str
)

serve(port=8081)
