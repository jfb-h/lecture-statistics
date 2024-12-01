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
        map(x -> [x[1], x[2]], zip(t, h))
    )
end

N, p1, p2 = 50, 0.5, 0.7

i = Observable(1)

y1 = simulate(N, p1)
y2 = simulate(N, p2)

pd(x, h, t; α=1, β=1) = pdf.(Beta(α + h, β + t), x);
pd(ht) = x -> pd(x, ht[1], ht[2])

function plot_coinflip(y1, y2)
    N = length(y1)
    fig = Figure(;size=(900, 500), backgroundcolor=:white)
    
    xticks = ([1,2], ["Kopf", "Zahl"])

    ax1 = Axis(fig[1, 1]; xticks,  ylabel = "Häufigkeit")
    ax2 = Axis(fig[1, 2]; xticks)
    ax3 = Axis(fig[2, 1]; xlabel = "p (W'keit Kopf)", ylabel = "Dichte")
    ax4 = Axis(fig[2, 2]; xlabel = "p (W'keit Kopf)", ylabel = "Dichte")
    
    xlims!(ax3, 0, 1)
    xlims!(ax4, 0, 1)
    
    ylims!(ax3, 0, 4)
    ylims!(ax4, 0, 4)
    
    y1_curr = @lift(y1[$i])
    y2_curr = @lift(y2[$i])
    
    p1_curr = @lift(pd(y1[$i]))
    p2_curr = @lift(pd(y2[$i]))
    
    barplot!(ax1, [1, 2], y1_curr; color = "tomato")
    barplot!(ax2, [1, 2], y2_curr; color = "cornflowerblue")
    
    lines!(ax3, 0:0.01:1, p1_curr; color = "tomato")
    lines!(ax4, 0:0.01:1, p2_curr; color = "cornflowerblue")
    
    return fig, ax1, ax2, ax3, ax4
end

fig, ax1, ax2, ax3, ax4 = plot_coinflip(y1, y2)
nframes = N
framerate = 2

record(fig, "coinflip.gif", 1:N;
       loop=0, framerate=framerate) do n
    i[] = n
    ax1.title = "Münze 1 ($n Würfe)"
    ax2.title = "Münze 2 ($n Würfe)"

    ax1.limits = (nothing, nothing, 0, 40)
    ax2.limits = (nothing, nothing, 0, 40)

    ax3.limits = (0, 1, 0, 10)
    ax4.limits = (0, 1, 0, 10)
end
