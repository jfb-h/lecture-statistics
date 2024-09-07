using Bonito: DOM, Bonito, Observables, App, Server, route!, Asset, Styles
using WGLMakie
using TidierDB, SQLite
import TidierData as TD
using TidierData: across, everything

include("components.jl")
include("theme.jl")
set_theme!(ThemeClean())

con = connect(sqlite(), db="../surveys/surveys.db")

function updatedata(con)
    @chain db_table(con, "news") begin
        @select(!id)
        @summarize(across(sum))
        @collect
    end
end

function updatedata(con)
    @chain db_table(con, "news") begin
        @select(!id)
        @collect
        TD.@pivot_longer(TD.everything())
        TD.@group_by(variable)
        TD.@summarize(count = sum(!ismissing(value)))
        TD.@arrange(variable)
    end
end

app = App(title="Survey results") do session
    xy = Observable(Point2f[Point2f(0)])
    fig = Figure()
    ax = Axis(fig[1, 1])
    Base.errormonitor(@async while true
        dat = updatedata(nothing)
        xy[] = Point2f.(dat.variable, dat.count)
        autolimits!(ax) # or just set fixed limits
        sleep(1)
        isopen(session) || break
    end)
    barplot!(ax, xy; color=:tomato)
    DOM.div(fig, style=Styles("flex" => "auto", "width" => "100vw", "height" => "100vh"))
end

server = Server("0.0.0.0", 8080; proxy_url="https://surveys.eggroup-lmu.de/statlecture-results/")
route!(server, "/session-01" => app)
server

#TODO: page_html could be good for sharing slides afterwards


