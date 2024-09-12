from fasthtml.common import *
from components import setup, Survey, Items, QRCode, NumericInput

def survey_livingcost(db, rt, route):
    setup(db, rt, route, "livingcost", cost=float)

    @rt(f"/{route}")
    def get():
        num = NumericInput("cost", "Wie viel gibst du montlich für's Wohnen aus?", "0", "10000")
        return Survey( "Kurzumfrage", Items(num, hx_post=f"/statlecture/{route}"))

