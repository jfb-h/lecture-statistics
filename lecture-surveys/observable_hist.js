import * as Plot from "https://cdn.jsdelivr.net/npm/@observablehq/plot@0.6/+esm";

function updateHistogram() {
    const container = document.getElementById('hist');
    const containerWidth = container.offsetWidth;
    const containerHeight = container.offsetHeight;

    fetch('stats')
    .then(response => response.json())
    .then(data => {
        const plot = Plot.plot({
            width: containerWidth,
            height: containerHeight,

            marks: [
                Plot.barY(data.dists, Plot.binX({y: "count"}, {x: d => d}))
            ],
            x: { label: "Distanz (km)" },
            y: { label: "Häufigkeit" }
        });
        document.getElementById('hist').innerHTML = "";
        document.getElementById('hist').appendChild(plot);

        document.getElementById("n").innerText = data.n;
        document.getElementById("meandist").innerText = data.meandist;
    });
}

updateHistogram();
setInterval(updateHistogram, 2500);
