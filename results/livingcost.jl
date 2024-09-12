function updatedata(con)
    @chain db_table(con, "livingcost") begin
        @select(cost)
        @collect
    end
end

livingcost(con) = App() do session
    xy = Observable(Float64[900])
    n = lift(length, xy)
    s = lift(r(2) ∘ sum, xy)
    m = lift(r(2) ∘ mean, xy)

    fig = Figure()
    ax = Axis(fig[1, 1];
              # title="Wie viel gibst du monatlich für's Wohnen aus?",
              xlabel="Wohnkosten (Euro)",
              ylabel="Häufigkeit"
        )

    Base.errormonitor(@async while true
        # update data
        table = db_table(con, "livingcost")
        dat = @chain table begin
            @select(cost)
            @collect
        end
        # update observable
        if length(dat.cost) > 0
            xy[] = dat.cost
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
        bignum(s; header=D.i("Summe"), footer=L(raw"\Sigma_{i=1}^N x_i")),
        bignum(m; header=D.i("Mittelwert"), footer=L(raw"\bar{x} = \frac{1}{N}\Sigma_{i=1}^N x_i"))
    )

    titled("Ergebnisse", grid(cards, card(fig); columns="1fr 3fr"))
end

