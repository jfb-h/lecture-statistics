using Bonito
using WGLMakie

app() = App() do session
    xy = Observable(Float64[100])

    fig = Figure()
    ax = Axis(fig[1, 1])

    Base.errormonitor(@async while true
        dat = rand(100)
        xy[] = dat
        autolimits!(ax)
        sleep(1)
        isopen(session) || break
    end)

    hist!(ax, xy)
    DOM.div(fig)
end

server = Server("49.12.228.148", 1234)
route!(server, "/test" => app())
server

