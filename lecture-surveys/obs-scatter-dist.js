import * as Plot from "https://cdn.jsdelivr.net/npm/@observablehq/plot@0.6/+esm";

const dep_lat = 48.1475;
const dep_lon = 11.5644;

let n_old = 0;
let dists = [];

function haversine(lat1, lon1, lat2, lon2) {
    if (lat1 == null || lon1 == null || lat2 == null || lon2 == null) { return null; };
    const R = 6371;
    const toRad = (value) => value * Math.PI / 180;

    const dLat = toRad(lat2 - lat1);
    const dLon = toRad(lon2 - lon1);

    const a = Math.sin(dLat / 2) ** 2 + Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon / 2) ** 2;
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    return R * c;
}

function updateData(route) {
    fetch(route)
    .then(response => response.json())
    .then(data => {
        let n_new = data.length;

        if (n_new == n_old) {
            console.log("No data changes");
            return;
        }

        data.slice(n_old).forEach(point => {
            let dist_current = haversine(dep_lat, dep_lon, point.lat_current, point.lon_current)
            let dist_before = haversine(dep_lat, dep_lon, point.lat_before, point.lon_before)
            dists.push({dist_current: dist_current, dist_before: dist_before})
        });

        n_old = n_new;
    })
    .catch(error => { console.error("Error fetching data:", error); });
}

function updateScatter() {
    const containerScatter = document.getElementById('scatter');
    const containerScatterWidth = containerScatter.offsetWidth;
    const containerScatterHeight = containerScatter.offsetHeight;

    const plotScatter = Plot.plot({
        width: containerScatterWidth,
        height: containerScatterHeight,
        style: {fontSize: "16px"},

        marks: [
            Plot.dot(dists, {x: "dist_current", y: "dist_before"}),
            Plot.crosshair(dists, {x: "dist_current", y: "dist_before"}),
            Plot.axisX({label: "Distanz zur Uni", lineWidth: 8, marginBottom: 40})
        ],
        y: { label: "Umzugsdistanz" }
    });

    containerScatter.innerHTML = "";
    containerScatter.appendChild(plotScatter);
}

updateData('data');
updateScatter();

setInterval(x => updateData('data'), 1000);
setInterval(x => updateScatter(), 1000);
