using Bonito: Observables, App, Server, route!, Asset, browser_display, Button
using Bonito.DOM: div, h1
using WGLMakie
using SQLite, DBInterface
using DataFrames: DataFrame

include("components.jl")
include("theme.jl")
set_theme!(ThemeClean())
# browser_display()

const con = SQLite.DB("../survey/interests.db")

function plotdata(dat)
    f, a, p = scatter(dat; SCATTER_ARGS...)
    xlims!(a, 0, 11)
    ylims!(a, 0, 11)
    f
end

function getdata(con)
    res = DBInterface.execute(con, "SELECT interesse, vorkenntnisse FROM items") |> DataFrame
    [Point2f(row.vorkenntnisse, row.interesse) for row in eachrow(res)]
end

app = makeapp(con) do dat
    f, a, p = scatter(dat; SCATTER_ARGS...)
    xlims!(a, 0, 11)
    ylims!(a, 0, 11)
    f
end

server = Server(app, "0.0.0.0", 8080)
