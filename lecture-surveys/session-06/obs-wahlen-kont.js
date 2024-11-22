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

let answers = [];
function updateData(data) {
    answers = data;
}

function chiSquared(data) {
    const usCategories = [...new Set(data.map(d => d.media))];
    const dCategories = [...new Set(data.map(d => d.wahl_d))];

    const contingencyTable = {};
    usCategories.forEach(us => {
        contingencyTable[us] = {};
        dCategories.forEach(d => {
            contingencyTable[us][d] = 0;
        });
    });

    data.forEach(d => {
        contingencyTable[d.media][d.wahl_d]++;
    });

    const rowTotals = {};
    const colTotals = {};
    let total = 0;

    usCategories.forEach(us => {
        rowTotals[us] = 0;
        dCategories.forEach(d => {
            rowTotals[us] += contingencyTable[us][d];
            colTotals[d] = (colTotals[d] || 0) + contingencyTable[us][d];
            total += contingencyTable[us][d];
        });
    });

    let chiSquared = 0;
    usCategories.forEach(us => {
        dCategories.forEach(d => {
            const observed = contingencyTable[us][d];
            const expected = (rowTotals[us] * colTotals[d]) / total;
            chiSquared += Math.pow(observed - expected, 2) / expected;
        });
    });

    return chiSquared
}

function contingencyCoefficient(data) {
    const n = data.length
    const chiSq = chiSquared(data);
    return Math.sqrt(chiSq / (chiSq + n))
}

function plot() {
    const container = document.getElementById('wahlen');
    const containerWidth = container.offsetWidth;
    const containerHeight = container.offsetHeight;

    const container_heat = document.getElementById('wahlen_heat');
    const container_heatWidth = container_heat.offsetWidth;
    const container_heatHeight = container_heat.offsetHeight;

    const chi = chiSquared(answers);
    const con = contingencyCoefficient(answers);

    const fmt = d3.format(".2f");

    document.getElementById('c4').innerHTML = `<strong>${fmt(chi)}</strong><br>`;
    document.getElementById('c5').innerHTML = `<strong>${fmt(con)}</strong><br>`;

    const media_plot = Plot.plot({
        height: 300,
        marginBottom: 50,
        width: containerWidth,
        x: {
            label: null,
            domain: ["Soc. Media", "Zeitung DE", "Zeitung Int", "TV / Radio", "Sonstige"],
        },
        y: {
            label: "Anzahl",
        },
        marks: [
            Plot.barY(answers, Plot.groupX({ y: "count" }, { x: "media" }))
        ],
    });

    const d_plot = Plot.plot({
        height: 300,
        width: containerWidth,
        x: {
            label: null,
            domain: ["Union", "SPD", "Gruene", "FDP", "AfD", "Sonstige"],
        },
        y: {
            label: "Anzahl",
        },
        marks: [
            Plot.barY(answers, Plot.groupX({ y: "count" }, { x: "wahl_d" }))
        ],
    });


    const heat_plot = Plot.plot({
        width: container_heatWidth,
        height: 600,
        style: { fontSize: "16px" },
        marginLeft: 70,
        marginRight: 50,
        marginBottom: 120,
        marginTop: 50,
        inset: 20,

        x: {
            label: null,
            domain: ["Soc. Media", "Zeitung DE", "Zeitung Int", "TV / Radio", "Sonstige"],
            tickRotate: 90
        },
        y: {
            label: null,
            domain: ["Union", "SPD", "Gruene", "FDP", "AfD", "Sonstige"],
        },
        color: { label: "Anzahl", legend: true, scheme: "YlGnBu" },
        marks: [
            Plot.cell(answers, Plot.group({ fill: "count" }, { fill: "count", x: "media", y: "wahl_d" }))
        ]
    });

    container.innerHTML = "";
    container.appendChild(media_plot);
    container.appendChild(d_plot);

    container_heat.innerHTML = "";
    container_heat.appendChild(heat_plot);


}

window.addEventListener('resize', debounce(() => { plot(); }, 100));

updatePlot(plot);
setInterval(() => updatePlot(plot), 1000);
