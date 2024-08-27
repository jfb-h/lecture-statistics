# app = App() do session
#     # css = Asset("https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css")
#     but = Button("Update")
#     dat = Observable(Point2f[])
#     on(but.value) do click
#         dat[] = getdata(con)
#     end
#     fig = plotdata(dat)
#     div(but, fig)
# end

function makeapp(plotfun, con::SQLite.DB; interval=1)
    App(title="Survey results") do session
        # css = Asset("https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css")
        dat = Observable(Point2f[])
        but = Button("Start/Stop")
        clicked = Observable(false)
        function fetch_data()
            while clicked[]
                dat[] = getdata(con)
                sleep(interval)
            end
        end
        on(but.value) do _
            @show clicked[]
            if clicked[]
                clicked[] = false
            else
                clicked[] = true
                @async fetch_data()
            end
        end
        div(but, plotfun(dat))
    end
end
