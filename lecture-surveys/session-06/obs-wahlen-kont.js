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

function correctedContingencyCoefficient(data) {
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

    const correctedCoefficient = Math.sqrt(chiSquared / (chiSquared + total));
    return correctedCoefficient;
}

function createSummary(data) {
    const ftm = d3.format(".2f");
    const pcor = correctedContingencyCoefficient(answers)
    return `Pearson korrigiert: <strong>${ftm(pcor)}</strong><br>`
}

function plot() {
    const container = document.getElementById('wahlen');
    const container_heat = document.getElementById('wahlen_heat');
    const containerWidth = container.offsetWidth;
    const containerHeight = container.offsetHeight;
    const container_heatWidth = container_heat.offsetWidth;
    const container_heatHeight = container_heat.offsetHeight;

    document.getElementById('c2').innerHTML = createSummary(answers);

    const media_counts = answers.reduce((acc, curr) => {
        acc[curr.media] = (acc[curr.media] || 0) + 1;
        return acc;
    }, {});

    const media_data = Object.entries(media_counts).map(([media, count]) => ({
        media,
        count,
    }));

    const d_counts = answers.reduce((acc, curr) => {
        acc[curr.wahl_d] = (acc[curr.wahl_d] || 0) + 1;
        return acc;
    }, {});


    const d_data = Object.entries(d_counts).map(([party, count]) => ({
        party,
        count,
    }));

    const media_plot = Plot.plot({
        height: 300,
        width: containerWidth,
        x: {
            label: null,
            domain: ["Soc. Media", "Zeitung DE", "Zeitung Int", "TV / Radio", "Sonstige"],
        },
        y: {
            label: "Anzahl",
        },
        marks: [
            Plot.barY(media_data, { x: "media", y: "count", fill: "steelblue" })
        ],
        color: { legend: true }
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
            Plot.barY(d_data, { x: "party", y: "count", fill: "orange" })
        ],
        color: { legend: true }
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
