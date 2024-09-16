from fasthtml.common import *
from news import survey_news
from livingcost import survey_livingcost
from earnings import survey_earnings

db = database("surveys.db")
app, rt = fast_app(live=True)

survey_news(db, rt, "nachrichten")
survey_livingcost(db, rt, "wohnen")
survey_earnings(db, rt, "einkommen")

serve(port=8081)
