from fasthtml.common import *
from news import survey_news
from livingcost import survey_livingcost

db = database("surveys.db")
app, rt = fast_app(live=True)

survey_news(db, rt, "news")
survey_livingcost(db, rt, "livingcost")

serve(port=8081)
