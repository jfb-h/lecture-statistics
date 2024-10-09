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

// Dont change this
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

// adapt this to data used in plot

const parser = d3.timeParse("%H:%M");

let plotdata = [];
function updateData(data) {
    const dep_lat = 48.1475;
    const dep_lon = 11.5644;

    data.slice(n_old).forEach(point => {
        let dist_current = haversine(dep_lat, dep_lon, point.lat_current, point.lon_current)
        plotdata.push({ dist: dist_current, time: parser(point.time) })
    });
}

function plot() {
    console.log(plotdata)
    const container = document.getElementById('plot-dist-time');
    const containerWidth = container.offsetWidth;
    const containerHeight = container.offsetHeight;

    const p = Plot.plot({
        width: containerWidth,
        height: containerHeight - 50,
        style: { fontSize: "16px" },
        marginLeft: 50,
        marginRight: 50,
        marginBottom: 50,
        marginTop: 50,
        inset: 20,
        color: {
            label: "Häufigkeit",
            scheme: "YlGnBu",
            legend: true,
            marginRight: 10,
            width: 500,
            height: 50,
        },

        marks: [
            Plot.rect(
                plotdata,
                Plot.bin({ fill: "count" }, { x: "dist", y: "time" })
            )
        ],
        x: { label: "Distanz zur Uni (km)" },
        y: { label: "Uhrzeit", },
    });

    container.innerHTML = "";
    container.appendChild(p);
}

window.addEventListener('resize', debounce(() => { plot(); }, 100));

updatePlot(plot);
setInterval(_ => updatePlot(plot), 1000);

