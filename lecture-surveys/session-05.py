from fasthtml.common import *
import json
import dataclasses
import polars as pl
from components import Survey, Items, QRCode, PlotContainer, StyledGrid, StyledCard, Choice, Radio, NumericInput

# überflutungsrisiko

def choice_lage(name, title):
    return Choice(
        Radio(name, "AM", "Arithmetisches Mittel"),
        Radio(name, "GM", "Geometrisches Mittel"),
        Radio(name, "Median", "Median"),
        Radio(name, "Modus", "Modus"),
        title=title
    )

def choice_streuung(name, title):
    return Choice(
        Radio(name, "SD", "Standardabweichung"),
        Radio(name, "MAD", "MAD"),
        Radio(name, "Entropie", "Entropie"),
        Radio(name, "Dissens", "Dissens"),
        title=title
    )

# SURVEY measures

def init_measures(db, rt, route, tablename, **kwargs):
    table = db.t[tablename]
    if table not in db.t:
        table.create(id=int, pk="id", **kwargs)

    Item = table.dataclass()

    # SURVEY FORM AND POST SPEC

    @rt(f"/{route}")
    def get():
        q1 = H4("Fall 1: Landnutzungstypen")

        d1 = P("""
        Die UNECE Unterscheidet in ihrer Klassifikation von Landnutzungstypen folgende
         Gruppen:

        (a) agricultural land,
        (b) forest and other wooded land,
        (c) built—up and related land, excluding scattered farm buildings,
        (d) wet open land,
        (e) dry open land with special vegetation cover,
        (f) open land without, or with insignificant, vegetation cover, and
        (g) waters.

        Welche Maße nutzen Sie, um die Flächennutzung von Bayern und NRW zu vergleichen?
        """)

        l1 = choice_lage("Landnutzung_lage", "Lage")
        s1 = choice_streuung("Landnutzung_streuung", "Streuung")

        q2 = H4("Fall 2: Vertrauen in die Politik")

        d2 = P("""
        Die European Social Survey befragt Haushalte unter anderem zu Themen wie Vertrauen in Politik und Wissenschaft.
        Dabei kommt eine 11-Punkte-Skala zum Einsatz, die von 'No trust at all' bis 'complete trust' reicht. Welche Maße
        nutzen Sie, um das Vertrauen der Bevölkerung in die Politik über europäische Staaten hinweg zu vergleichen?
        """)

        l2 = choice_lage("Vertrauen_lage", "Lage")
        s2 = choice_streuung("Vertrauen_streuung", "Streuung")

        items = Items(
            q1, d1, l1, s1,
            q2, d2, l2, s2,
            hx_post=f"/statlecture/{route}"
        )

        q3 = H4("Fall 3: Temperaturveränderungen")

        d3 = P("""
        Sie haben Daten zur mittleren Tagestemperatur und möchten saisonale Temperaturunterschiede im Jahresverlauf und die Variabilität über die letzten 50 Jahre für den Standort München bewerten. Welche Maße setzen Sie ein?
        """)

        l3 = choice_lage("Temperatur_lage", "Lage")
        s3 = choice_streuung("Temperatur_streuung", "Streuung")

        items = Items(
            q1, d1, l1, s1,
            q2, d2, l2, s2,
            q3, d3, l3, s3,
            hx_post=f"/statlecture/{route}"
        )
        return Survey("Lage und Streuung", items)

    @rt(f"/{route}")
    def post(item: Item):
        table.insert(item)
        return Strong("Danke für deine Antwort!")

    @rt(f"/{route}/qr")
    def get(): return QRCode(f"{route}")

    @rt(f"/{route}/data")
    async def get():
        df = pl.read_database("SELECT * FROM measures", db).unpivot(index='id')

        df = (
            df.with_columns(
                pl.col("variable").str.split("_").alias("split_variable")
            )
            .with_columns([
                pl.col("split_variable").list.get(0).alias("variable"),
                pl.col("split_variable").list.get(1).alias("measure")
            ])
            .drop("split_variable")
        )
        return df.write_json()


    update_data = ScriptX("session-01/fetch-data.js")
    obs_results = ScriptX("session-05/obs-measures.js", type="module")

    @rt(f"/{route}/results")
    async def get():
        plot = StyledCard(
            PlotContainer(id="results"),
            header=H2("Welche Maße setzen Sie ein?"),
        )
        grid = StyledGrid(plot)
        return Title("Einführung"), Main(grid, update_data, obs_results, cls="container")



# SERVER AND DB INITIALIZATION 

db = database("surveys.db")
app, rt = fast_app(live=True)

init_measures(
    db, rt, "measures", "measures",
    Landnutzung_lage = str, Landnutzung_streuung = str,
    Vertrauen_lage = str, Vertrauen_streuung = str,
    Temperatur_lage = str, Temperatur_streuung = str,
)

serve(port=8081)
