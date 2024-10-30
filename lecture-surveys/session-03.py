
from fasthtml.common import *
import json
import dataclasses
from components import Survey, Items, QRCode, PlotContainer, StyledGrid, StyledCard, Choice, Radio, NumericInput


# SURVEY LIVINGCOST

def init_livingcost(db, rt, route, tablename, **kwargs):
    table = db.t[tablename]
    if table not in db.t:
        table.create(id=int, pk="id", **kwargs)

    Item = table.dataclass()

    @rt(f"/{route}")
    def get():
        num = NumericInput("kosten", "Wie viel gibst du montlich für's Wohnen aus?", "0", "10000000")

        choice = Choice(
            Radio("wohnsituation", "Familie", "Ich wohne bei meiner Familie"),
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

        c1 = Card(Div(id="c1"), header=Strong("Alleine"), style="height: 1fr")
        c2 = Card(Div(id="c2"), header=Strong("Familie"), style="height: 1fr")
        c3 = Card(Div(id="c3"), header=Strong("WG"), style="height: 1fr")

        grid = Grid(Div(c1, c2, c3), plot,
            style = f"grid-template-columns: 1fr 4fr; grid-template-rows: none; height: 90vh;"
        )

        hdr = H2("Wie viel geben Studierende in München für das Wohnen aus?")

        return Title("Einführung"), Main(hdr, grid, update_data, obs_results, cls="container")


    obs_results_relative = ScriptX("session-03/obs-livingcost-relative.js", type="module")

    @rt(f"/{route}/results-geometric")
    async def get():
        plot = StyledCard(
            PlotContainer(id="wohnsituation-gm")
        )

        c1 = Card(Div(id="c1-gm"), header=Strong("Alleine"), style="height: 1fr")
        c2 = Card(Div(id="c2-gm"), header=Strong("Familie"), style="height: 1fr")
        c3 = Card(Div(id="c3-gm"), header=Strong("WG"), style="height: 1fr")

        grid = Grid(Div(c1, c2, c3), plot,
            style = f"grid-template-columns: 1fr 4fr; grid-template-rows: none; height: 90vh;"
        )

        hdr = H2("Wie viel geben Studierende in München im Verhältnis zu Studierenden in Heidelberg (538€) aus?")

        return Title("Lagemaße"), Main(hdr, grid, update_data, obs_results_relative, cls="container")


    obs_results_median = ScriptX("session-03/obs-livingcost-median.js", type="module")

    @rt(f"/{route}/results-median")
    async def get():
        plot = StyledCard(
            Div(Span("AM mit Prinz", style="color: red"), " | ", Span("AM ohne Prinz", style="color: blue")), 
            PlotContainer(id="wohnsituation-median")
        )

        grid = StyledGrid(plot)

        return Title("Lagemaße"), Main(grid, update_data, obs_results_median, cls="container")


# SERVER AND DB INITIALIZATION 

db = database("surveys.db")
app, rt = fast_app(live=True)

init_livingcost(
    db, rt, "wohnsituation", "wohnsituation",
    kosten=float, wohnsituation=str
)

serve(port=8081)

