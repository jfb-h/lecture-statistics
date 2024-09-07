from fasthtml.common import *
from components import Items, QRCode, Slider, Choice, MultiChoice

db = database("surveys.db")
app, rt = fast_app(live=True)

news = db.t.news
if news not in db.t: news.create(id=int, social_media=str, zeitung_de=str, zeitung_int=str, tv_radio=str, andere=str, pk="id")
News = news.dataclass()

@rt("/session-01/news")
def get():
    mult = MultiChoice(
        Choice("social_media", "Social Media (z.B. Instagram, TikTok, Facebook)"),
        Choice("zeitung_de", "Deutschsprachige Zeitungen (z.B. FAZ, Zeit, Sueddeutsche, TAZ, NZZ)"),
        Choice("zeitung_int", "Internationale Zeitungen (z.B. Guardian, NYT, Economist, LeMonde)"),
        Choice("tv_radio", "TV oder Radio"),
        Choice("andere", "Andere"),
        title="Welche Quellen nutzt du primär, um dich über aktuelle Ereignisse zu informieren?",
    )
    return Titled(
        "Kurzumfrage",
        Hr(), Items(mult, hx_post="/statlecture/session-01/news"), # have to set full path for htmx somehow
        style={"max-width": "600px"})

@rt("/session-01/news")
def post(newsitem: News):
    news.insert(newsitem)
    return Strong("Danke für deine Antwort!")

@rt("/session-01/news/qr")
def get(): return QRCode("session-01/news")

serve(port=8081)

