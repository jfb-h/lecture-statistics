from math import radians, sin, cos, sqrt, atan2
from fasthtml.common import *
import pgeocode
import json
import random

from components import setup, Survey, Items, QRCode, TextInput, TimeInput, NumericInput, SelectInput, PlotContainer

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

pico_leaflet = StyleX("session-01/pico-leaflet.css")
update_data = ScriptX("session-01/fetch-data.js")

leaflet_app = ScriptX("session-01/leaflet-map-dists.js")
observable_hist = ScriptX("session-01/obs-hist-dist.js", type="module")
observable_scatter = ScriptX("session-01/obs-scatter-dist.js", type="module")
observable_hist_times = ScriptX("session-01/obs-hist-getuptime.js", type="module")

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
        ti = TimeInput("time", "Wann bist du heute morgen aufgestanden?", "z.B. 06:30")
        gr = NumericInput("note", "Wie viele Punkte hattest du im Abitur in Mathe?", 0, 15)

        nf = SelectInput("nebenfach",
            Option("Biologie", value="Biologie"),
            Option("Experimentalphysik", value="Experimentalphysik"),
            Option("Geophysik", value="Geophysik"),
            Option("Künstliche Intelligenz", value="KI"),
            Option("Informatik", value="Informatik"),
            Option("Meteorologie", value="Meteorologie"),
            Option("Politikwissenschaften", value="Politik"),
            Option("Soziologie", value="Soziologie"),
            Option("Statistik", value="Statistik"),
            Option("Volkswirtschaftslehre", value="VWL"),
            Option("Betriebswirtschaftslehre", value="BWL"),
        )

        return Survey("Kurzumfrage", Items(pc, pb, ti, gr, nf, hx_post=f"/statlecture/{route}"))


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
        return Strong("Danke für deine Antwort!")


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
        return json.dumps([{
            "lat_current": item.lat_current,
            "lon_current": item.lon_current,
            "lat_before": item.lat_before,
            "lon_before": item.lon_before,
            "time": item.time,
        } for item in table()])


    @rt(f"/{route}/map")
    async def get():
        map_current = Card(
            PlotContainer(id="map-current"),
            header=H2(Span("Wohnort aktuell"), Span(id="n-map-current")),
            style="display: flex; flex-direction: column; height: 95%; width: 100%;",
        )

        map_before  = Card(
            PlotContainer("map-before"),
            header=H2(Span("Wohnort während des Abiturs"), Span(id="n-map-before")),
            style="display: flex; flex-direction: column; height: 95%; width: 100%;",
        )

        grid = Grid(map_current, map_before, style = "grid-template-columns: 1fr 1fr; grid-template-rows: none; height: 95vh")

        return Title("Wohnorte"), Main(grid, update_data, leaflet_app, cls="container")


    @rt(f"/{route}/hist")
    async def get():
        hist_current = Card(
            PlotContainer("hist-current"),
            header=H2(Span("Weg zur Uni"), Span(id="n-hist-current")),
            style="display: flex; flex-direction: column; height: 95%; width: 100%;",
        )

        hist_before = Card(
            PlotContainer("hist-before"),
            header=H2(Span("Umzugsdistanz"), Span(id="n-hist-before")),
            style="display: flex; flex-direction: column; height: 95%; width: 100%;",
        )

        grid = Grid(
            hist_current, hist_before,
            style = "grid-template-columns: 1fr 1fr; grid-template-rows: none; height: 95vh"
        )

        return Title("Wohnorte"), Main(grid, update_data, observable_hist, cls="container")


    @rt(f"/{route}/scatter")
    async def get():
        scatter = Card(
            PlotContainer(id="scatter"),
            header=H2("Wohnen weithergezogene Studierende näher an der Uni?"),
            footer=Label(Input(type="checkbox", id="check-regression"), "Lineare Regression"),
            style="display: flex; flex-direction: column; height: 95%; width: 100%;",
        )

        grid = Grid(
            scatter,
            style = "grid-template-columns: 1fr; grid-template-rows: none; height: 95dvh"
        )

        return Title("Wohnorte"), Main(grid, update_data, observable_scatter, cls="container")


    @rt(f"/{route}/qr")
    def get(): return QRCode(f"{route}")



    @rt(f"/{route}/getuptime")
    async def get():
        hist = Card(
            PlotContainer("hist-getuptime"),
            header=H2("Wann bist du heute morgen aufgestanden?"),
            style="display: flex; flex-direction: column; height: 95%; width: 100%;",
        )

        grid = Grid(
            hist,
            style = "grid-template-columns: 1fr; grid-template-rows: none; height: 95dvh"
        )

        return Title("Wohnorte"), Main(grid, update_data, observable_hist_times, cls="container")


    @rt(f"/{route}/qr")
    def get(): return QRCode(f"{route}")


def survey_place(db, rt, route):
    setup_postalcodes(db, rt, route, "wohnort",
                      lat_current=float, lon_current=float,
                      lat_before=float, lon_before=float,
                      place_current=str, place_before=str,
                      time=str, nebenfach=str, mathenote=int)


db = database("surveys.db")
app, rt = fast_app(live=True, hdrs=(leaflet_css, leaflet_js, pico_leaflet))
survey_place(db, rt, "wohnort")
serve(port=8081)

