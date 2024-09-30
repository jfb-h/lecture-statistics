function livingcost(con)
    App(title="Wohnen") do session

        g1 = Observable(Float64[900])
        g2 = Observable(Float64[900])
        g3 = Observable(Float64[900])

        n1 = lift(length, g1)
        n2 = lift(length, g2)
        n3 = lift(length, g3)

        s1 = lift(Int ∘ r(0) ∘ sum, g1)
        s2 = lift(Int ∘ r(0) ∘ sum, g2)
        s3 = lift(Int ∘ r(0) ∘ sum, g3)

        m1 = lift(r(1) ∘ mean, g1)
        m2 = lift(r(1) ∘ mean, g2)
        m3 = lift(r(1) ∘ mean, g3)

        fig = Figure()

        ax1 = Axis(fig[1, 1]; title="Alleine")
        ax2 = Axis(fig[2, 1]; title="Eltern", ylabel="Häufigkeit")
        ax3 = Axis(fig[3, 1]; title="WG", xlabel="Wohnkosten (Euro)")

        xlims!(ax1, 0, 2000)
        xlims!(ax2, 0, 2000)
        xlims!(ax3, 0, 2000)

        linkxaxes!(ax1, ax2, ax3)

        hidexdecorations!(ax1; grid=false)
        hidexdecorations!(ax2; grid=false)

        i = 1

        Base.errormonitor(@async while true
            # update data
            dat = DBInterface.execute(con,
                "select kosten, wohnsituation from wohnen;"
            ) |> DataFrame
            # update observable
            if length(dat.kosten) > 0
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
        hist!(ax2, g2; color=:darkslateblue, strokewidth=1, strokecolor=:white)
        hist!(ax3, g3; color=:gold, strokewidth=1, strokecolor=:white)


        vlines!(ax1, lift(mean, g1); color=:grey, linewidth=3, linestyle=:dash, label="Mittelwert")
        vlines!(ax2, lift(mean, g2); color=:grey, linewidth=3, linestyle=:dash, label="Mittelwert")
        vlines!(ax3, lift(mean, g3); color=:grey, linewidth=3, linestyle=:dash, label="Mittelwert")

        # axislegend(ax1; position=:rt)

        s(x, y, z) = D.p(
            D.span(x; style="color: tomato"), " ",
            D.span(y, style="color: darkslateblue"), " ",
            D.span(z; style="color: gold")
        )

        cards = D.div(
            D.h3("Berechnung des Mittelwerts"),
            bignum(s(n1, n2, n3); header=D.i("Anzahl"), footer=L(raw"N")),
            bignum(s(s1, s2, s3); header=D.i("Summe"), footer=L(raw"\Sigma_{i=1}^N x_i")),
            bignum(s(m1, m2, m3); header=D.i("Mittelwert"), footer=L(raw"\bar{x} = \frac{1}{N}\Sigma_{i=1}^N x_i"))
        )

        grd = grid(cards, card(fig); columns="1fr 3fr")

        titled("Ergebnisse", grd)
    end
end

