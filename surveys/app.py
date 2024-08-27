from fasthtml.common import *
from components import Slider, Items

# connect to database
db = database("surveys.db")

# new database table for survey
interests = db.t.interests
if interests not in db.t: interests.create(id=int, interesse=int, vorkenntnisse=int, pk="id")
Answer = interests.dataclass()

# app and routing definition
app, rt = fast_app(live=True)

# store posted form in database
@rt("/statlecture/session-01") # have to set full path for htmx somehow
def post(answer: Answer):
    interests.insert(answer)
    return Strong("Danke für deine Antwort!")

# form with survey items
@rt("/session-01")
def get():
    q1 = Slider("interesse",
                "1. Wie groß ist dein Interesse an Statistik?",
                "sehr niedrig", "sehr hoch")

    q2 = Slider("vorkenntnisse",
                "2. Wie würdest du deine Vorkenntnisse in Statistik einschätzen?",
                "sehr schlecht", "sehr gut")

    return Titled("Survey | Einführung in die Statistik",
                  Hr(), Items(q1, q2, port="statlecture/session-01"),
                  style={"max-width": "600px"})

serve(port=8081)

