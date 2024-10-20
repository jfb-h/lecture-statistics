import * as Plot from "https://cdn.jsdelivr.net/npm/@observablehq/plot@0.6/+esm";

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

// adapt these to the data used in the plot
let grades = [];
function updateData(data) {
    grades = data;
}

function plot() {
    const container = document.getElementById('hist-grade');
    const containerWidth = container.offsetWidth;
    const containerHeight = container.offsetHeight;

    const p = Plot.plot({
        width: containerWidth,
        height: containerHeight,
        style: { fontSize: "16px" },
        marginLeft: 50,
        marginRight: 50,
        marginBottom: 50,
        marginTop: 50,

        marks: [
            // Plot.barY(grades, Plot.groupX({ y: "count" }, { x: "grade" })),
            Plot.dot(grades, Plot.stackY2({ x: "grade", y: (_) => 1, fill: "black" })),
            Plot.ruleY([0])
        ],
        x: { label: "Punkte im Abitur", domain: [...Array(16).keys()] },
        y: { label: "Häufigkeit", grid: true }
    });


    container.innerHTML = "";

    container.appendChild(p);
}

window.addEventListener('resize', debounce(() => { plot(); }, 100));

updatePlot(plot);
setInterval(() => updatePlot(plot), 1000);
