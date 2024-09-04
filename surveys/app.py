from fasthtml.common import *
from components import Slider, Items, QRCode, Check, MultiCheck

db = database("surveys.db")

app, rt = fast_app(live=True)

news = db.t.news
if news not in db.t: news.create(id=int, social_media=str, zeitungen_de=str, zeitungen_int=str, andere=str, pk="id")
News = news.dataclass()

@rt("/session-01/news")
def get():
    mult = MultiCheck(
        Check("social_media", "Social Media (z.B. Instagram, TikTok, Facebook)"),
        Check("zeitung_de", "Deutschsprachige Zeitungen (z.B. FAZ, Zeit, Sueddeutsche, TAZ, NZZ)"),
        Check("zeitung_int", "Internationale Zeitungen (z.B. Guardian, NYT, Economist, LeMonde)"),
        Check("tv_radio", "TV oder Radio"),
        Check("andere", "Andere"),
        title="Welche Quellen nutzt du primär, um dich über aktuelle Ereignisse zu informieren?",
    )
    return Titled("Kurzumfrage",
                  Hr(), Items(mult, hx_post="/statlecture/session-01/news"), # have to set full path for htmx somehow
                  style={"max-width": "600px"})

@rt("/session-01/news")
def post(newsitem: News):
    news.insert(newsitem)
    return Strong("Danke für deine Antwort!")

@rt("/session-01/news/qr")
def get(): return QRCode("session-01")

serve(port=8081)

