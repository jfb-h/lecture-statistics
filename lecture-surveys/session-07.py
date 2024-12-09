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


def init_randomnumbers(db, rt, route, tablename, **kwargs):
    # DATABASE SETUP

    table = db.t[tablename]
    if table not in db.t:
        table.create(id=int, pk="id", **kwargs)

    Item = table.dataclass()

    # SURVEY FORM AND POST SPEC

    @rt(f"/{route}")
    def get():
        va = NumericInput("vara", "Eine zufällige Zahl zwischen 0 und 50?", min=0, max=50)
        vb = NumericInput("varb", "Noch eine zufällige Zahl zwischen 0 und 50?", min=0, max=50)
        
        items = Items(va, vb, hx_post=f"/{route}")
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

    observable_barchart = ScriptX("session-07/obs-randomnumbers.js", type="module")

    @rt(f"/{route}/result")
    async def get():
        barchart1 = PlotContainer(id="plot1")
        barchart2 = PlotContainer(id="plot2")
        barchart3 = PlotContainer(id="plot3")
            
        grid = Grid(
            Div(barchart1, style=f"position: absolute;top: 0;left: 0; width: 50%"), 
            Div(barchart2, style=f"position: absolute;top: 0;right: 0;width: 50%"), 
            Div(barchart3, style=f"position: absolute;bottom: 0;left: 0;height: 50%")
        )

        return Title("Ergebnis"), Main(grid, update_data, observable_barchart, cls="container")



# SERVER AND DB INITIALIZATION 

db = database("surveys.db")

app, rt = fast_app(live=True, hdrs=(leaflet_css, leaflet_js, pico_leaflet))
init_randomnumbers(db, rt, "randomnumbers", "randomnumbers", vara=float, varb=float)

serve(port=8081)
