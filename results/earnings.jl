earnings(con) =
    App() do session
        xy = Observable(Float64[900])
        n = lift(length, xy)
        s = lift(r(2) ∘ sum, xy)
        m = lift(r(2) ∘ mean, xy)

        fig = Figure()
        ax = Axis(fig[1, 1]; xlabel="Einkommen (Euro)", ylabel="Häufigkeit")
        xlims!(ax, 0, 2000)

        Base.errormonitor(@async while true
            # update data
            dat = DBInterface.execute(con, "select einkommen from einkommen;") |> DataFrame
            # update observable
            if length(dat.einkommen) > 0
                xy[] = dat.einkommen
            end

            autolimits!(ax)
            sleep(1)
            isopen(session) || break
        end)

        hist!(ax, xy; color=:tomato, strokewidth=1, strokecolor=:white)
        vlines!(ax, m; color=:navyblue, linewidth=3, linestyle=:dash, label="Mittelwert")
        axislegend(ax; position=:rt)

        cards = D.div(
            D.h3("Berechnung des Mittelwerts"),
            bignum(n; header=D.i("Anzahl"), footer=L(raw"N")),
            bignum(m; header=D.i("Mittelwert"), footer=L(raw"\bar{x} = \frac{1}{N}\Sigma_{i=1}^N x_i")),
            bignum(m; header=D.i("Median"))
        )

        grd = grid(cards, card(fig); columns="1fr 3fr")

        titled("Ergebnisse", grd)
    end
