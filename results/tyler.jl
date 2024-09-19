using Bonito, Tyler, WGLMakie
using Tyler.MapTiles

WGLMakie.activate!(; resize_to=:parent)

App() do session
    fig = Figure()
    ax = Axis(fig[1, 1])

    ger = Rect2f(7.0, 47.0, 5.17, 8.0)
    tyler = Tyler.Map(ger; figure=fig, axis=ax)

    hidedecorations!(ax)
    hidespines!(ax)

    convert_point(lat, lon) = MapTiles.project((lon, lat), MapTiles.wgs84, MapTiles.web_mercator)

    makepoints() = [Point2f(convert_point(rand(47.0:0.1:55.0), rand(5.5:0.1:15.0))) for _ in 1:100]
    points = Observable(makepoints())
    munich = Point2f(convert_point(48.1374, 11.5755))
    lines = lift(pts -> map(p -> (munich, p), pts), points)

    @async while true
        points[] = makepoints()
        sleep(1)
    end

    p = scatter!(ax, points; color="black")
    l = linesegments!(ax, lines; color=(:black, 0.5), linewidth=0.7)

    translate!(p, 0, 0, 100)
    translate!(l, 0, 0, 100)

    DOM.div(fig; style="width:100vw; height:100vh")
end

