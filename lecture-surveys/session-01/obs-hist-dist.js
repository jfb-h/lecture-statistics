import * as Plot from "https://cdn.jsdelivr.net/npm/@observablehq/plot@0.6/+esm";
import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";

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

function haversine(lat1, lon1, lat2, lon2) {
    const R = 6371;
    const toRad = (value) => value * Math.PI / 180; // Helper function to convert degrees to radians

    const dLat = toRad(lat2 - lat1);
    const dLon = toRad(lon2 - lon1);

    const a = Math.sin(dLat / 2) ** 2 + Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon / 2) ** 2;
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    return R * c;
}

// adapt these to the data used in the plot
let counter_current = 0;
let counter_before = 0;

let dist_current = [];
let dist_before = [];

// this gets called only through updatePlot
function updateData(data) {
    const dep_lat = 48.1475;
    const dep_lon = 11.5644;

    data.slice(n_old).forEach(point => {
        if (point.lat_current !== null && point.lon_current !== null) {
            let d = haversine(dep_lat, dep_lon, point.lat_current, point.lon_current)
            dist_current.push(d);
            counter_current += 1;
        }
        if (point.lat_before !== null && point.lon_before !== null) {
            let d = haversine(dep_lat, dep_lon, point.lat_before, point.lon_before)
            dist_before.push(d);
            counter_before += 1;
        }
    });
}

function histograms() {
    const containerBefore = document.getElementById('hist-before');
    const containerBeforeWidth = containerBefore.offsetWidth;
    const containerBeforeHeight = containerBefore.offsetHeight;

    const containerCurrent = document.getElementById('hist-current');
    const containerCurrentWidth = containerCurrent.offsetWidth;
    const containerCurrentHeight = containerCurrent.offsetHeight;


    // get quartiles to make domain depend in IQR
    const values = dist_current
        .filter(v => v != null)
        .sort((a, b) => a - b);

    const q1 = d3.quantile(values, 0.25);
    const q2 = d3.quantile(values, 0.50);
    const q3 = d3.quantile(values, 0.75);
    const iqr = q3 - q1;

    document.getElementById("n-hist-current").innerText = " (n = " + counter_current + ")";
    document.getElementById("n-hist-before").innerText = " (n = " + counter_before + ")";

    const plotCurrent = Plot.plot({
        width: containerCurrentWidth,
        height: containerBeforeHeight,
        style: {fontSize: "16px"},
        marginBottom: 40,
        marginTop: 40,

        marks: [
            Plot.rectY(dist_current, Plot.binX({y: "count"}, {x:  {value: (d) => d, interval: 1}})),
            Plot.ruleY([0])
        ],
        x: { label: "Distanz (km)", domain: [0, q2 + 3.5 * iqr]},
        y: { label: "Häufigkeit" }
    });

    const plotBefore = Plot.plot({
        width: containerBeforeWidth,
        height: containerBeforeHeight,
        style: {fontSize: "16px"},
        marginBottom: 40,
        marginTop: 40,

        marks: [
            Plot.rectY(dist_before, Plot.binX({y: "count"}, {x: d => d})),
            Plot.ruleY([0])
        ],
        x: { label: "Distanz (km)"},
        y: { label: "Häufigkeit" }
    });

    containerBefore.innerHTML = "";
    containerCurrent.innerHTML = "";

    containerBefore.appendChild(plotBefore);
    containerCurrent.appendChild(plotCurrent);
}

window.addEventListener('resize', debounce(() => { histograms(); }, 100));

updatePlot(histograms);
setInterval(x => updatePlot(histograms), 1000);
