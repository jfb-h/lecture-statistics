from fasthtml.common import *
from components import setup, Survey, Items, QRCode, NumericInput

def survey_earnings(db, rt, route):
    setup(db, rt, route, "einkommen", einkommen=float)
    @rt(f"/{route}")
    def get():
        des = P("Dein Einkommen beschreibt die Gesamtmenge an Geld, die monatlich auf deinem Konto eingeht.")
        num = NumericInput("einkommen", "Was ist dein monatliches Einkommen?", "0", "10000000")
        return Survey("Kurzumfrage", Items(des, num, hx_post=f"/statlecture/{route}"))

