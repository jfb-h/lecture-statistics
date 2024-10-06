import * as Plot from "https://cdn.jsdelivr.net/npm/@observablehq/plot@0.6/+esm";
import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";

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

// dont change this
let n_old = 0;
function updatePlot(plotfun) {
    if (surveydata.length > n_old) {
        updateData(surveydata);
        n_old = surveydata.length;
        plotfun();
    } else {
        return;
    }
}

// adapt this to the plotting data
let dists = [];
function updateData(data) {
    const dep_lat = 48.1475;
    const dep_lon = 11.5644;

    data.slice(n_old).forEach(point => {
        let dist_current = haversine(dep_lat, dep_lon, point.lat_current, point.lon_current)
        let dist_before = haversine(dep_lat, dep_lon, point.lat_before, point.lon_before)
        dists.push({ dist_current: dist_current, dist_before: dist_before })
    });
}

function scatter() {
    const containerScatter = document.getElementById('scatter');
    const containerScatterWidth = containerScatter.offsetWidth;
    const containerScatterHeight = containerScatter.offsetHeight;

    const max_before = d3.max(dists.map(d => d.dist_before));
    const max_current = d3.max(dists.map(d => d.dist_current));

    const plotScatter = Plot.plot({
        width: containerScatterWidth,
        height: containerScatterHeight,
        style: { fontSize: "16px" },
        marginLeft: 60,
        marginRight: 50,
        marginBottom: 50,
        marginTop: 50,
        inset: 20,

        marks: [
            Plot.dot(dists, { y: "dist_current", x: "dist_before" }),
            Plot.crosshair(dists, { y: "dist_current", x: "dist_before", color: "blue" }),
            isoline.checked ? Plot.link({ length: 1 }, { x1: 0, x2: 500, y1: 0, y2: 500, stroke: "black", strokeOpacity: 0.2 }) : [],
            regression.checked ? Plot.linearRegressionY(dists, { y: "dist_current", x: "dist_before" }) : []
        ],
        x: { label: "Umzugsdistanz (km)", domain: [0, max_before] },
        y: { label: "Distanz zur Uni (km)", domain: [0, max_current] },
    });

    containerScatter.innerHTML = "";
    containerScatter.appendChild(plotScatter);
}

const regression = document.getElementById('check-regression');
const isoline = document.getElementById('check-isoline');

document.getElementById('check-regression')
    .addEventListener('change', () => { scatter(); });

document.getElementById('check-isoline')
    .addEventListener('change', () => { scatter(); });

window.addEventListener('resize', debounce(() => { scatter(); }, 100));

updatePlot(scatter);
setInterval(_ => updatePlot(scatter), 1000);

