using Bonito

const leafletjs = Bonito.ES6Module("https://esm.sh/v133/leaflet@1.9.4/es2022/leaflet.mjs")
const leafletcss = Bonito.Asset("https://unpkg.com/leaflet@1.9.4/dist/leaflet.css")

mutable struct LeafletMap
    position::NTuple{2,Float64}
    zoom::Int
end

function Bonito.jsrender(session::Session, map::LeafletMap)
    map_div = DOM.div(id="map"; style="height: 900px;")
    return Bonito.jsrender(session, DOM.div(
        leafletcss,
        leafletjs,
        map_div,
        js"""
            $(leafletjs).then(L => {
                window.m = L.map('map').setView($(map.position), $(map.zoom));

                L.tileLayer(
                    'https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    maxZoom: 19,
                    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                }).addTo(m)
            })
        """
    ))
end

App() do session
    map = LeafletMap((50.147, 11.564), 6)
    makepoint() = [rand(47.0:0.1:55.0), rand(5.5:0.1:15.0)]
    points = Observable(makepoint())

    update_points = js"""p => {
        $(leafletjs).then(L => {
            if (window.m != null) {
                L.marker(p).addTo(window.m);
            }
        })
    }"""

    onjs(session, points, update_points)

    @async while true
        points[] = makepoint()
        sleep(1)
    end

    return map
end
