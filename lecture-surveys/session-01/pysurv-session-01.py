from math import radians, sin, cos, sqrt, atan2
from fasthtml.common import *
import pgeocode
import json
import random
from components import setup, Survey, Items, QRCode, TextInput, TimeInput

nomi = pgeocode.Nominatim('de')

N_SIM = 1

def simulate():
    # Germany
    ger_lat_min = 47.2701  # Southern latitude
    ger_lat_max = 55.0581  # Northern latitude
    ger_lon_min = 5.8663   # Western longitude
    ger_lon_max = 15.0419  # Eastern longitude

    # Munich
    muc_lat_min = 48.028
    muc_lat_max = 48.227
    muc_lon_min = 11.450
    muc_lon_max = 11.686

    lat_current = random.uniform(muc_lat_min, muc_lat_max)
    lon_current = random.uniform(muc_lon_min, muc_lon_max)

    lat_before = random.uniform(ger_lat_min, ger_lat_max)
    lon_before = random.uniform(ger_lon_min, ger_lon_max)

    return {
        'lat_current': lat_current, 'lon_current': lon_current,
        'lat_before': lat_before, 'lon_before': lon_before
    }


leaflet_css = Link( rel = "stylesheet", href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css")
leaflet_js = Script(src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js")

pico_leaflet = StyleX("pico_leaflet.css")
leaflet_app = ScriptX("leaflet_app.js")
observable_hist = ScriptX("observable_hist.js", type="module")
observable_scatter = ScriptX("scatter.js", type="module")
observable_hist_times = ScriptX("hist-times.js", type="module")

def setup_postalcodes(db, rt, route, tablename, **kwargs):
    table = db.t[tablename]
    if table not in db.t:
        table.create( id=int, pk="id", **kwargs)

    Item = table.dataclass()

    @dataclass
    class PostalCodes:
        pc_current: str
        pc_before: str
        time: str

    @rt(f"/{route}")
    def get():
        pc = TextInput("pc_current", "Was ist die PLZ deines aktuellen Wohnortes?", "z.B. 80333")
        pb = TextInput("pc_before", "Was ist die PLZ deines Wohnortes während des Abiturs?", "z.B. 40229")
        pt = TimeInput("time", "Wann bist du heute morgen aufgestanden?", "z.B. 06:30")
        return Survey("Kurzumfrage", Items(pc, pb, pt, hx_post=f"/statlecture/{route}"))


    @rt(f"/{route}")
    def post(item: PostalCodes):
        pc = nomi.query_postal_code(item.pc_current)
        pb = nomi.query_postal_code(item.pc_before)

        i = Item()

        i.lat_current=pc.latitude
        i.lon_current=pc.longitude
        i.lat_before=pb.latitude
        i.lon_before=pb.longitude
        i.place_current=pc.place_name
        i.place_before=pb.place_name
        i.time = item.time

        table.insert(i)
        Strong("Danke für deine Antwort!")


    @rt(f"/{route}/simulate")
    async def get():
        global N_SIM
        N_SIM += 1
        if N_SIM > 300:
            return json.dumps([simulate() for i in range(300)])
        else:
            return json.dumps([simulate() for i in range(N_SIM)])


    @rt(f"/{route}/data")
    async def get():
        """
        post lat/lon data as json for leaflet
        """
        return json.dumps([{
            "lat_current": item.lat_current,
            "lon_current": item.lon_current,
            "lat_before": item.lat_before,
            "lon_before": item.lon_before,
        } for item in table()])


    @rt(f"/{route}/map")
    async def get():
        map_current = Card(
            Div(id="map-current", style="flex-grow: 1; height: 0;"),
            header=H2(Span("Wohnort aktuell"), Span(id="n-map-current")),
            style="display: flex; flex-direction: column; height: 95%; width: 100%;",
        )

        map_before  = Card(
            Div(id="map-before", style="flex-grow: 1; height: 0;"),
            header=H2(Span("Wohnort während des Abiturs"), Span(id="n-map-before")),
            style="display: flex; flex-direction: column; height: 95%; width: 100%;",
        )

        grid = Grid(map_current, map_before, style = "grid-template-columns: 1fr 1fr; grid-template-rows: none; height: 95vh")

        return Title("Wohnorte"), Main(grid, leaflet_app, cls="container")


    @rt(f"/{route}/hist")
    async def get():
        hist_current = Card(
            Div(id="hist-current", style="flex-grow: 1; height: 0;"),
            header=H2(Span("Weg zur Uni"), Span(id="n-hist-current")),
            style="display: flex; flex-direction: column; height: 95%; width: 100%;",
        )

        hist_before = Card(
            Div(id="hist-before", style="flex-grow: 1; height: 0;"),
            header=H2(Span("Umzugsdistanz"), Span(id="n-hist-before")),
            style="display: flex; flex-direction: column; height: 95%; width: 100%;",
        )

        grid = Grid(
            hist_current, hist_before,
            style = "grid-template-columns: 1fr 1fr; grid-template-rows: none; height: 95vh"
        )

        return Title("Wohnorte"), Main(grid, observable_hist, cls="container")


    @rt(f"/{route}/scatter")
    async def get():
        scatter = Card(
            Div(id="scatter", style="flex-grow: 1; height: 0;"),
            header=H2("Wohnen weithergezogene Studierende näher an der Uni?"),
            style="display: flex; flex-direction: column; height: 95%; width: 100%;",
        )

        grid = Grid(
            scatter,
            style = "grid-template-columns: 1fr; grid-template-rows: none; height: 95dvh"
        )

        return Title("Wohnorte"), Main(grid, observable_scatter, cls="container")


    @rt(f"/{route}/qr")
    def get(): return QRCode(f"{route}")



    @rt(f"/{route}/times")
    async def get():
        hist = Card(
            Div(id="hist-times", style="flex-grow: 1; height: 0;"),
            header=H2(""),
            style="display: flex; flex-direction: column; height: 95%; width: 100%;",
        )

        grid = Grid(
            hist,
            style = "grid-template-columns: 1fr; grid-template-rows: none; height: 95dvh"
        )

        return Title("Wohnorte"), Main(grid, observable_hist_times, cls="container")


    @rt(f"/{route}/qr")
    def get(): return QRCode(f"{route}")


def survey_place(db, rt, route):
    setup_postalcodes(db, rt, route, "wohnort",
          lat_current=float, lon_current=float,
          lat_before=float, lon_before=float,
          place_current=str, place_before=str, 
          time=str)


db = database("surveys.db")
app, rt = fast_app(live=True, hdrs=(leaflet_css, leaflet_js, pico_leaflet))
survey_place(db, rt, "wohnort")
serve(port=8081)
