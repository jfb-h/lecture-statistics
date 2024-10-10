from fasthtml.common import *  # Link, Script, StyleX, ScriptX, Option,
import pgeocode
import json
import dataclasses
from helpers import simulate_latlon
from components import Survey, Items, QRCode, TextInput, TimeInput, NumericInput, SelectInput, PlotContainer, StyledGrid, StyledCard

nomi = pgeocode.Nominatim("de")
N_SIM = 1

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
        pc = TextInput("pc_current", "Was ist die PLZ deines aktuellen Wohnortes?", "z.B. 80333")
        pb = TextInput("pc_before", "Was ist die PLZ deines Wohnortes während des Abiturs?", "z.B. 40229")
        ti = TimeInput("time", "Wann bist du heute morgen aufgestanden?", "z.B. 06:30", min="00:00", max="08:00")
        gr = NumericInput("grade", "Wie viele Punkte [0-15] hattest du im Abitur in Mathe?", min=0, max=15)

        nf = SelectInput(
            "minor",
            "Was ist dein Nebenfach?",
            Option("Biologie", value="Biologie"),
            Option("Geophysik", value="Geophysik"),
            Option("Meteorologie", value="Meteorologie"),
            Option("Experimentalphysik", value="Experimentalphysik"),
            Option("Statistik", value="Statistik"),
            Option("Informatik", value="Informatik"),
            Option("Künstliche Intelligenz", value="KI"),
            Option("Soziologie", value="Soziologie"),
            Option("Politikwissenschaften", value="Politik"),
            Option("Volkswirtschaftslehre", value="VWL"),
            Option("Betriebswirtschaftslehre", value="BWL"),
            Option("Andere", value="Andere"),
        )

        return Survey("Kurzumfrage", Items(ti, pc, pb, gr, nf, hx_post=f"/statlecture/{route}"))

    # This is necessary because we convert postal codes
    # to lat/lon before storing them in the DB.
    @dataclass
    class PostalCodes:
        pc_current: str
        pc_before: str
        time: str
        grade: int
        minor: str

    @rt(f"/{route}")
    def post(item: PostalCodes):
        pc = nomi.query_postal_code(item.pc_current)
        pb = nomi.query_postal_code(item.pc_before)

        i = Item()

        i.lat_current = pc.latitude
        i.lon_current = pc.longitude
        i.lat_before = pb.latitude
        i.lon_before = pb.longitude
        i.place_current = pc.place_name
        i.place_before = pb.place_name
        i.time = item.time
        i.grade = item.grade
        i.minor = item.minor

        table.insert(i)
        return Strong("Danke für deine Antwort!")

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

    leaflet_app = ScriptX("session-01/leaflet-map-dists.js")

    @rt(f"/{route}/map")
    async def get():
        map_current = StyledCard(
            PlotContainer(id="map-current"),
            header=H2(Span("Wohnort aktuell"), Span(id="n-map-current")),
        )
        map_before = StyledCard(
            PlotContainer("map-before"),
            header=H2(Span("Wohnort Abitur"), Span(id="n-map-before")),
        )
        grid = StyledGrid(map_current, map_before, columns="1fr 1fr")
        return Title("Einführung"), Main(grid, update_data, leaflet_app, cls="container")


    observable_hist = ScriptX("session-01/obs-hist-dist.js", type="module")

    @rt(f"/{route}/hist")
    async def get():
        hist_current = StyledCard(
            PlotContainer("hist-current"),
            header=H2(Span("Weg zur Uni"), Span(id="n-hist-current")),
        )
        hist_before = StyledCard(
            PlotContainer("hist-before"),
            header=H2(Span("Umzugsdistanz"), Span(id="n-hist-before")),
        )
        grid = StyledGrid(hist_current, hist_before, columns="1fr 1fr")
        return Title("Einführung"), Main(grid, update_data, observable_hist, cls="container")


    observable_scatter = ScriptX("session-01/obs-scatter-dist.js", type="module")

    @rt(f"/{route}/scatter")
    async def get():
        scatter = StyledCard(
            PlotContainer(id="scatter"),
            header=H2("Wohnen weithergezogene Studierende näher an der Uni?"),
            footer=Div(
                Label(Input(type="checkbox", id="check-isoline"), "Isolinie", style="padding: 2px 10px"),
                Label(Input(type="checkbox", id="check-regression"), "Lineare Regression", style="padding: 2px 10px"),
                style="display: flex"
            )
        )
        grid = StyledGrid(scatter)
        return Title("Einführung"), Main(grid, update_data, observable_scatter, cls="container")


    observable_hist_times = ScriptX("session-01/obs-hist-getuptime.js", type="module")

    @rt(f"/{route}/getuptime")
    async def get():
        hist = StyledCard(
            PlotContainer("hist-getuptime"),
            header=H2("Wann bist du heute morgen aufgestanden?"),
        )
        grid = StyledGrid(hist)
        return Title("Einführung"), Main(grid, update_data, observable_hist_times, cls="container")


    observable_boxp_grade = ScriptX("session-01/obs-boxp-grade.js", type="module")

    @rt(f"/{route}/boxplot")
    async def get():
        plot = StyledCard(
            PlotContainer("boxplot-grade"),
            header=H2("Beeinflussen Erfahrungen mit Schulmathematik die Nebenfachwahl?"),
            footer=Div(
                Label(Input(type="checkbox", id="check-boxordot"), "Boxplot", style="padding: 2px 10px"),
                style="display: flex"
            )
        )
        grid = StyledGrid(plot)
        return Title("Einführung"), Main(grid, update_data, observable_boxp_grade, cls="container")


    observable_scatter_time = ScriptX("session-01/obs-scatter-dist-time.js", type="module")

    @rt(f"/{route}/scatter-time")
    async def get():
        scatter = StyledCard(
            PlotContainer(id="plot-dist-time"),
            header=H2("Wer muss am frühesten aufstehen?"),
        )
        grid = StyledGrid(scatter)
        return Title("Einführung"), Main(grid, update_data, observable_scatter_time, cls="container")


    observable_map_dens = ScriptX("session-01/obs-map-dens.js", type="module")

    @rt(f"/{route}/density")
    async def get():
        plot = StyledCard(
            PlotContainer("density-map"),
            header=H2("Kerndichteschätzung der Studierendenherkunft"),
        )
        grid = StyledGrid(plot)
        return Title("Einführung"), Main(grid, update_data, observable_map_dens, cls="container")


# SERVER AND DB INITIALIZATION 

route = "wohnort"
table = "wohnort"

db = database("surveys.db")

app, rt = fast_app(live=True, hdrs=(leaflet_css, leaflet_js, pico_leaflet))

init_app(db, rt, route, table, lat_current=float, lon_current=float, lat_before=float, lon_before=float, place_current=str, place_before=str, time=str, minor=str, grade=int)

serve(port=8081)
