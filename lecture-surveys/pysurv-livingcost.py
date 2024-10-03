from fasthtml.common import *
from components import setup, Survey, Items, QRCode, NumericInput, Choice, Radio

def survey_livingcost(db, rt, route):
    setup(db, rt, route, "wohnen", kosten=float, wohnsituation=str)

    @rt(f"/{route}")
    def get():
        num = NumericInput("kosten", "Wie viel gibst du montlich für's Wohnen aus?", "0", "10000")

        choice = Choice(
            Radio("wohnsituation", "eltern", "Ich wohne bei meinen Eltern / meiner Familie"),
            Radio("wohnsituation", "alleine", "Ich wohne alleine"),
            Radio("wohnsituation", "wg", "Ich wohne in einer WG"),
            Radio("wohnsituation", "andere", "Andere"),
            title="Was trifft auf deine Wohnsituation zu?",
        )

        return Survey( "Kurzumfrage", Items(num, choice, hx_post=f"/statlecture/{route}"))
