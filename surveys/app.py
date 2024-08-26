from fasthtml.common import *
from components import Slider, Items
from fh_altair import altair_headers, altair2fasthml
import altair as alt

# connect to database
db = database("surveys.db")

# new database table for survey
interests = db.t.interests
if interests not in db.t: interests.create(id=int, interesse=int, vorkenntnisse=int, pk="id")
Answer = interests.dataclass()

# app and routing definition
app, rt = fast_app(live=True, hdrs=altair_headers)

# store posted from in database
@rt("/")
def post(answer: Answer):
    interests.insert(answer)
    return Strong("Danke für deine Antwort!")

# form with survey items
@rt("/")
def get():
    q1 = Slider("interesse",
                "1. Wie groß ist dein Interesse an Statistik?",
                "sehr niedrig", "sehr hoch")

    q2 = Slider("vorkenntnisse",
                "2. Wie würdest du deine Vorkenntnisse in Statistik einschätzen?",
                "sehr schlecht", "sehr gut")

    return Titled("Survey | Einführung in die Statistik",
                  Hr(), Items(q1, q2),
                  style={"max-width": "600px"})

# plot the result
def plotdata(db):
    data = db.q("SELECT * FROM interests")
    p = alt.Chart(alt.Data(values=data)).mark_point().encode(
        x='interesse:Q',
        y='vorkenntnisse:Q'
    ).properties(width=1200, height=600).interactive()
    return altair2fasthml(p)

# serve the plot
@rt("/results")
def get():
    return Titled("Ergebnisse", plotdata(db))

# serve the app
serve(port=8081)
