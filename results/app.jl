using Bonito: Bonito, Observables, App, Server, route!, Asset, Styles, browser_display, Button
using Bonito.DOM: div, h1
using WGLMakie
using SQLite, DBInterface
using DataFrames: DataFrame

include("components.jl")
include("theme.jl")
set_theme!(ThemeClean())

const con = SQLite.DB("../surveys/surveys.db")

function getdata(con)
    query = "SELECT interesse, vorkenntnisse FROM interests"
    res = DBInterface.execute(con, query) |> DataFrame
    [Point2f(row.vorkenntnisse, row.interesse) for row in eachrow(res)]
end

app = makeapp(con; interval=1) do dat
    f, a, p = scatter(dat; SCATTER_ARGS...)
    a.title = "Ergebnis der Kurzumfrage"
    a.xlabel = "Interesse"
    a.ylabel = "Vorkenttnisse"
    xlims!(a, -1, 11)
    ylims!(a, -1, 11)
    f
end

server = Server("0.0.0.0", 8080;
                proxy_url="https://surveys.eggroup-lmu.de/statlecture-results/")

route!(server, "/session-01" => app)
# wait(server)
server

#TODO: page_html could be good for sharing slides afterwards


