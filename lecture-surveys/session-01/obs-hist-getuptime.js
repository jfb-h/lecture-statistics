import * as Plot from "https://cdn.jsdelivr.net/npm/@observablehq/plot@0.6/+esm";
import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";

const parser = d3.timeParse("%H:%M");

// function generateUTCTimestamps() {
//     const timestamps = [];
//
//     const today = new Date();
//     const start = new Date(Date.UTC(today.getUTCFullYear(), today.getUTCMonth(), today.getUTCDate(), 6, 0, 0));
//     const end = new Date(Date.UTC(today.getUTCFullYear(), today.getUTCMonth(), today.getUTCDate(), 8, 0, 0));
//
//     let current = start;
//     while (current <= end) {
//       timestamps.push(current.toISOString());
//       current = new Date(current.getTime() + 5 * 60 * 1000);
//     }
//
//     return timestamps;
// }

function updateData(route) {
    fetch(route)
    .then(response => response.json())
    .
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

        n_old = n_new;
    })
    .catch(error => { console.error("Error fetching data:", error); });
}

const eventTimestamps = generateUTCTimestamps();
console.log(eventTimestamps);

const events = eventTimestamps.map(d => new Date(d));

const container = document.getElementById('hist-times');
const containerWidth = container.offsetWidth;
const containerHeight = container.offsetHeight;

const histogram = Plot.plot({
    width: containerWidth,
    height: containerHeight,
    marks: [
        Plot.rectY(events, Plot.binX({y: "count"}, {
            x: d => d, 
            thresholds: d3.utcMinute.every(15) 
        }))
    ],
    x: {
        label: "Zeit",
        tickFormat: d3.utcFormat("%H:%M"),
    },
    y: {
        label: "Anzahl der Ereignisse",
    },
    width: 800,
    height: 400,
});

container.innerHTML = "";
container.appendChild(histogram);
