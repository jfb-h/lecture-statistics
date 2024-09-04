using Bonito: Bonito, Observables, App, Server, route!, Asset, Styles, browser_display, Button
using Bonito.DOM: div, h1
using WGLMakie
using SQLite, DBInterface
using TidierDB
import TidierData as TD

include("components.jl")
include("theme.jl")
set_theme!(ThemeClean())

con = connect(sqlite(), db="../surveys/surveys.db")

initdata(con) = @collect(db_table(con, "news"))

function updatedata(con)
    @chain db_table(con, "news") begin
        @select(!id)
        @collect
        TD.@pivot_longer(TD.everything())
        TD.@group_by(variable)
        TD.@summarize(count=sum(!ismissing(value)))
        TD.@arrange(variable)
    end
end

function plotdata(dat)
    y = @lift($dat.variable)
    x = @lift($dat.count)
    barplot(Categorical(y), y)
end

app = makeapp(plotdata, con; interval=1)

# server = Server("0.0.0.0", 8080;
#                 proxy_url="https://surveys.eggroup-lmu.de/statlecture-results/")
#
# route!(server, "/session-01" => app)
# # wait(server)
# server

#TODO: page_html could be good for sharing slides afterwards


