from math import radians, sin, cos, sqrt, atan2
from fasthtml.common import *
import pgeocode
import json
from components import setup, Survey, Items, QRCode, TextInput

nomi = pgeocode.Nominatim('de')

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

leaflet_css = Link( rel = "stylesheet", href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css")
leaflet_js = Script(src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js")

pico_leaflet = StyleX("pico_leaflet.css")
leaflet_app = ScriptX("leaflet_app.js")
observable_hist = ScriptX("observable_hist.js", type="module")

def setup_postalcodes(db, rt, route, tablename, **kwargs):
    table = db.t[tablename]
    if table not in db.t:
        table.create( id=int, pk="id", **kwargs)

    Item = table.dataclass()

    @dataclass
    class PostalCodes:
        pc_current: str
        pc_before: str

    @rt(f"/{route}")
    def post(item: PostalCodes):
        """
        convert postal codes to lat/lon and insert into table
        """
        pc = nomi.query_postal_code(item.pc_current)
        pb = nomi.query_postal_code(item.pc_before)

        i = Item()

        i.lat_current=pc.latitude
        i.lon_current=pc.longitude
        i.lat_before=pb.latitude
        i.lon_before=pb.longitude
        i.place_current=pc.place_name
        i.place_before=pb.place_name

        table.insert(i)
        return Strong("Danke für deine Antwort!")

    @rt(f"/{route}/data")
    async def get():
        """
        post lat/lon data as json for leaflet
        """
        return json.dumps([{"lat": item.lat_current, "lon": item.lon_current} for item in table()])

    @rt(f"/{route}/stats")
    async def get():
        """
        compute stats and post as json to insert into DOM
        """
        dep_lat = 48.1475
        dep_lon = 11.5644

        items = db.q(f"""SELECT lat_current, lon_current FROM {tablename}
                     WHERE lat_current IS NOT NULL AND lon_current IS NOT NULL""")

        n = len(items)
        dists = [haversine(dep_lat, dep_lon, item['lat_current'], item['lon_current']) for item in items]
        meandist = sum(dists) / n if n > 0 else 0

        return json.dumps({"n": n, "dists": dists, "meandist": round(meandist, 2)})

    @rt(f"/{route}/hist")
    async def get():
        """
        leaflet map app grid layout
        """

        cards = Div(
            H1("Distanz zum Department"),
            Card(Strong(id="n"), header=I("Anzahl")),
            Card(Strong(id="meandist"), Span(" km"), header=I("Mittelwert")),
        )
        
        hist = Card(Div(id="hist", style= "height: 100%; width: 100%;"), style="height: 95%; width: 100%;")
        grid = Grid(cards, hist, style = "grid-template-columns: 1fr 3fr; grid-template-rows: none; height: 95vh")

        return Title("Wohnorte"), Main(grid, observable_hist, cls="container")

    @rt(f"/{route}/map")
    async def get():
        """
        leaflet map app grid layout
        """

        cards = Div(
            H1("Distanz zum Department"),
            Card(Strong(id="n"), header=I("Anzahl")),
            Card(Strong(id="meandist"), Span(" km"), header=I("Mittelwert")),
        )
        
        map = Card(Div(id="map", style= "height: 100%; width: 100%;"), style="height: 95%; width: 100%;")
        grid = Grid(cards, map, style = "grid-template-columns: 1fr 3fr; grid-template-rows: none; height: 95vh")

        return Title("Wohnorte"), Main(grid, leaflet_app, cls="container")

    @rt(f"/{route}/qr")
    def get(): return QRCode(f"{route}")


def survey_place(db, rt, route):
    setup_postalcodes(db, rt, route, "wohnort",
          lat_current=float, lon_current=float,
          lat_before=float, lon_before=float,
          place_current=str, place_before=str)

    @rt(f"/{route}")
    def get():
        pc = TextInput("pc_current", "Was ist die PLZ deines aktuellen Wohnortes?", "z.B. 80333")
        pb = TextInput("pc_before", "Was ist die PLZ deines Wohnortes während des Abiturs?", "z.B. 40229")
        return Survey("Kurzumfrage", Items(pc, pb, hx_post=f"/statlecture/{route}"))

db = database("surveys.db")
app, rt = fast_app(live=True, hdrs=(leaflet_css, leaflet_js, pico_leaflet))

survey_place(db, rt, "wohnort")

serve(port=8081)
