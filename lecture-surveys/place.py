from fasthtml.common import *
import pgeocode
from components import setup, Survey, Items, QRCode, TextInput

nomi = pgeocode.Nominatim('de')

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

