function livingcost(con)
    App(title="Wohnen") do session
        xy = Observable(Float64[900])
        n = lift(length, xy)
        s = lift(r(2) ∘ sum, xy)
        m = lift(r(2) ∘ mean, xy)

        g1 = Observable(Float64[900])
        g2 = Observable(Float64[900])
        g3 = Observable(Float64[900])

        fig = Figure()

        ax1 = Axis(fig[1, 1]; title="Alleine")
        ax2 = Axis(fig[2, 1]; title="Eltern", ylabel="Häufigkeit")
        ax3 = Axis(fig[3, 1]; title="WG", xlabel="Wohnkosten (Euro)")

        xlims!(ax1, 0, nothing)
        xlims!(ax2, 0, nothing)
        xlims!(ax3, 0, nothing)

        ylims!(ax1, 0, nothing)
        ylims!(ax2, 0, nothing)
        ylims!(ax3, 0, nothing)

        linkxaxes!(ax1, ax2, ax3)

        hidexdecorations!(ax1; grid=false)
        hidexdecorations!(ax2; grid=false)

        i = 1

        Base.errormonitor(@async while true
            # update data
            table = db_table(con, "wohnen")
            dat = @chain table begin
                @select(kosten, wohnsituation)
                @collect
            end
            # update observable
            if length(dat.kosten) > 0
                xy[] = dat.kosten
                push!(g1[], randn() * 200 + 1400)
                push!(g2[], randn() * 200 + 200)
                push!(g3[], randn() * 200 + 900)
                # g1[] = dat.kosten[dat.wohnsituation.=="alleine"]
                # g2[] = dat.kosten[dat.wohnsituation.=="eltern"]
                # g3[] = dat.kosten[dat.wohnsituation.=="wg"]
                notify(g1)
                notify(g2)
                notify(g3)

                autolimits!(ax1)
                autolimits!(ax2)
                autolimits!(ax3)
            end

            i += 1
            i > 10000 && break

            sleep(0.7)
            isopen(session) || break
        end)

        hist!(ax1, g1; color=:tomato, strokewidth=1, strokecolor=:white)
        hist!(ax2, g2; color=:tomato, strokewidth=1, strokecolor=:white)
        hist!(ax3, g3; color=:tomato, strokewidth=1, strokecolor=:white)


        vlines!(ax1, lift(mean, g1); color=:navyblue, linewidth=3, linestyle=:dash, label="Mittelwert")
        vlines!(ax2, lift(mean, g2); color=:navyblue, linewidth=3, linestyle=:dash, label="Mittelwert")
        vlines!(ax3, lift(mean, g3); color=:navyblue, linewidth=3, linestyle=:dash, label="Mittelwert")

        # axislegend(ax1; position=:rt)

        cards = D.div(
            D.h3("Berechnung des Mittelwerts"),
            bignum(n; header=D.i("Anzahl"), footer=L(raw"N")),
            bignum(s; header=D.i("Summe"), footer=L(raw"\Sigma_{i=1}^N x_i")),
            bignum(m; header=D.i("Mittelwert"), footer=L(raw"\bar{x} = \frac{1}{N}\Sigma_{i=1}^N x_i"))
        )

        grd = grid(cards, card(fig); columns="1fr 3fr")

        titled("Ergebnisse", grd)
    end
end
