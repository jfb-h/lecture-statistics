from fasthtml.common import fast_app, serve, Strong, Titled, Hr
from components import Slider, Items
# from fh_altair import altair_headers, altair2fasthml
# import altair as alt

app, rt, answers, Answer = fast_app("interests.db", live=True,
                                    id=int, pk="id",
                                    interesse=int,
                                    vorkenntnisse=int,)

@rt("/")
def post(answer: Answer):
    answers.insert(answer)
    return Strong("Danke für deine Antwort!")

@rt("/")
def get():
    q1 = Slider("interesse",
                "1. Wie groß ist dein Interesse an Statistik?",
                "sehr niedrig", "sehr hoch")
    q2 = Slider("vorkenntnisse",
                "2. Wie würdest du deine Vorkenntnisse in Statistik einschätzen?",
                "sehr schlecht", "sehr gut")

    return Titled("Survey | Einführung in die Statistik", Hr(), Items(q1, q2), style={"max-width": "600px"})

serve()