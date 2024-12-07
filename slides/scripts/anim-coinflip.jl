using GLMakie
using GLMakie.Makie.Colors
using Distributions
Makie.inline!(true)
Makie.set_theme!(theme_light())

function simulate(N, p)
    c = rand(Bernoulli(p), N)
    h = cumsum(c)
    t = collect(1:N) .- h
    vcat(
        [[0,0]],
        map(x -> [x[1], x[2]], zip(h, t))
    )
end

function plot_coinflip(y1)
    fig = Figure(;size=(900, 500), padding=0)
    
    xticks = ([1,2], ["Kopf", "Zahl"])
    
    ax1 = Axis(fig[1, 1]; xticks,  ylabel = "Häufigkeit")
    ax3 = Axis(fig[1, 2]; xlabel = "θ", ylabel = "Dichte")
    
    ax1.limits = (nothing, nothing, 0, 40)
    ax3.limits = (0, 1, 0, 10)

    xlims!(ax3, 0, 1)
    ylims!(ax3, 0, 6)
    
    y1_curr = @lift(y1[$i])
    p1_curr = @lift(pd(y1[$i]))
    
    barplot!(ax1, [1, 2], y1_curr; color = "tomato")
    vlines!(ax3, 0.5; color = "black", linestyle = :dash)
    lines!(ax3, 0:0.01:1, p1_curr; color = "tomato")
    
    return fig, ax1, ax3
end

N, p1 = 50, 0.5
y1 = simulate(N, p1)

pd(x, h, t; α=1, β=1) = pdf.(Beta(α + h, β + t), x);
pd(ht) = x -> pd(x, ht[1], ht[2])

i = Observable(1)

fig, ax1, ax3 = plot_coinflip(y1)

record(fig, "coinflip.mp4", 1:N;
       loop=0, framerate=2) do n
    i[] = n

    ax1.title = "Beobachtungen (nach $n Würfen)"
    ax3.title = "Inferenz für θ"
end
