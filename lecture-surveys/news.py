from fasthtml.common import *
from components import setup, Survey, Items, QRCode, Slider, Choice, MultiChoice

def survey_news(db, rt, route):
    setup(db, rt, route, "news",
          social_media=int,
          zeitung_de=int,
          zeitung_int=int,
          tv_radio=int,
          andere=int,)

    @rt(f"/{route}")
    def get():
        mult = MultiChoice(
            Choice("social_media", "Social Media (z.B. Instagram, TikTok, Facebook)"),
            Choice( "zeitung_de", "Deutschsprachige Zeitungen (z.B. FAZ, Zeit, Sueddeutsche, TAZ, NZZ)",),
            Choice( "zeitung_int", "Internationale Zeitungen (z.B. Guardian, NYT, Economist, LeMonde)",),
            Choice("tv_radio", "TV oder Radio"),
            Choice("andere", "Andere"),
            title="Welche Quellen nutzt du primär, um dich über aktuelle Ereignisse zu informieren?",
        )
        # have to set full post path for htmx somehow
        return Survey( "Kurzumfrage", Items(mult, hx_post=f"/statlecture/{route}"))

