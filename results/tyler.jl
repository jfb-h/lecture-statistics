convert_point(lat, lon) = MapTiles.project((lon, lat), MapTiles.wgs84, MapTiles.web_mercator)
convert_point(p) = convert_point(p...)

function haversine(p1, p2)
    lat1, lon1 = p1
    lat2, lon2 = p2

    lat1_rad, lon1_rad = deg2rad(lat1), deg2rad(lon1)
    lat2_rad, lon2_rad = deg2rad(lat2), deg2rad(lon2)
    Δlat = lat2_rad - lat1_rad
    Δlon = lon2_rad - lon1_rad

    a = sin(Δlat / 2)^2 + cos(lat1_rad) * cos(lat2_rad) * sin(Δlon / 2)^2
    c = 2 * atan(sqrt(a), sqrt(1 - a))

    R = 6371.0
    R * c
end

function place_before(con)
    App() do session
        fig = Figure()
        ax = Axis(fig[1, 1])

        lat, lon, delta = 48.147, 11.564, 0.4
        ger = Rect2f(lon - delta / 2, lat - delta / 2, delta, delta)
        tyler = Tyler.Map(ger; figure=fig, axis=ax)

        hidedecorations!(ax)
        hidespines!(ax)
        xlims!(ax, nothing, nothing)

        points = Observable(Point2f[])
        dists = Observable(Float64[])
        munich = Point2f(convert_point(lat, lon))
        lines = lift(pts -> map(p -> (munich, p), pts), points)
        distmean = lift(r(2) ∘ mean, dists)
        n = lift(length, points)

        Base.errormonitor(@async while true
            dat = DBInterface.execute(con,
                "select lat_before as lat, lon_before as lon from wohnort
                 where lat is not null and lon is not null;"
            ) |> DataFrame
            points[] = map(Point2f ∘ convert_point, zip(dat.lat, dat.lon))
            dists[] = map(p -> haversine(Point2f(p...), Point2f(lat, lon)), zip(dat.lat, dat.lon))
            sleep(1)
        end)

        m = scatter!(ax, [munich]; marker='★', color=:gold, markersize=40, label="Department")
        p = scatter!(ax, points; color="orange", markersize=12, label="Wohnort")
        l = linesegments!(ax, lines; color=(:black, 0.5), linewidth=0.7, label="Luftlinie")

        axislegend(ax; position=:rb, orientation=:horizontal, labelsize=18)

        translate!(m, 0, 0, 98)
        translate!(l, 0, 0, 99)
        translate!(p, 0, 0, 100)

        cards = D.div(
            D.h3("Distanz zum Department"),
            bignum(n; header=D.i("Anzahl"), footer=L(raw"N")),
            bignum(D.span(distmean, " km"); header=D.i("Mittelwert"), footer=L(raw"\bar{x} = \frac{1}{N}\Sigma_{i=1}^N x_i")),
        )

        grd = grid(cards, card(D.div(fig; style="width:100%; height:100%")); columns="1fr 3fr")

        titled("Distanz zum Wohnort", grd)
    end
end

function place_current(con)
    App() do session
        fig = Figure()
        ax = Axis(fig[1, 1])

        lat, lon, delta = 48.147, 11.564, 0.4
        ger = Rect2f(lon - delta / 2, lat - delta / 2, delta, delta)
        tyler = Tyler.Map(ger; figure=fig, axis=ax)

        hidedecorations!(ax)
        hidespines!(ax)
        xlims!(ax, nothing, nothing)

        points = Observable(Point2f[])
        dists = Observable(Float64[])
        munich = Point2f(convert_point(lat, lon))
        lines = lift(pts -> map(p -> (munich, p), pts), points)
        distmean = lift(r(2) ∘ mean, dists)
        n = lift(length, points)

        Base.errormonitor(@async while true
            dat = DBInterface.execute(con,
                "select lat_current as lat, lon_current as lon from wohnort
                 where lat is not null and lon is not null;"
            ) |> DataFrame
            points[] = map(Point2f ∘ convert_point, zip(dat.lat, dat.lon))
            dists[] = map(p -> haversine(Point2f(p...), Point2f(lat, lon)), zip(dat.lat, dat.lon))
            sleep(1)
        end)

        m = scatter!(ax, [munich]; marker='★', color=:gold, markersize=40, label="Department")
        p = scatter!(ax, points; color="orange", markersize=12, label="Wohnort")
        l = linesegments!(ax, lines; color=(:black, 0.5), linewidth=0.7, label="Luftlinie")

        axislegend(ax; position=:rb, orientation=:horizontal, labelsize=18)

        translate!(m, 0, 0, 98)
        translate!(l, 0, 0, 99)
        translate!(p, 0, 0, 100)

        cards = D.div(
            D.h3("Distanz zum Department"),
            bignum(n; header=D.i("Anzahl"), footer=L(raw"N")),
            bignum(D.span(distmean, " km"); header=D.i("Mittelwert"), footer=L(raw"\bar{x} = \frac{1}{N}\Sigma_{i=1}^N x_i")),
        )

        grd = grid(cards, card(D.div(fig; style="width:100%; height:100%")); columns="1fr 3fr")

        titled("Distanz zum Wohnort", grd)
    end
end
