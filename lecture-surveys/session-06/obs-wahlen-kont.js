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

    const usCategories = [...new Set(data.map(d => d.wahl_us))];
    const dCategories = [...new Set(data.map(d => d.wahl_d))];
    
    const contingencyTable = {};
    usCategories.forEach(us => {
        contingencyTable[us] = {};
        dCategories.forEach(d => {
            contingencyTable[us][d] = 0;
        });
    });
    
    data.forEach(d => {
        contingencyTable[d.wahl_us][d.wahl_d]++;
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
    const containerWidth = container.offsetWidth;
    const containerHeight = container.offsetHeight;
    
    document.getElementById('c2').innerHTML = createSummary(answers);

    const us_counts = answers.reduce((acc, curr) => {
        acc[curr.wahl_us] = (acc[curr.wahl_us] || 0) + 1;
        return acc;
    }, {});
    
    const us_data = Object.entries(us_counts).map(([candidate, count]) => ({
        candidate,
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
    
    const us_plot = Plot.plot({
        height: 300,
        width: 400,
        x: {
            label: "US Candidates",
            domain: ["harris", "trump"],
        },
        y: {
            label: "Votes",
        },
        marks: [
            Plot.barY(us_data, { x: "candidate", y: "count", fill: "steelblue" })
        ],
        color: { legend: true }
    });
    
    const d_plot = Plot.plot({
        height: 300,
        width: 400,
        x: {
            label: "German Parties",
            domain: ["union", "spd", "gr", "fdp", "afd", "sonstige"],
        },
        y: {
            label: "Votes",
        },
        marks: [
            Plot.barY(d_data, { x: "party", y: "count", fill: "orange" })
        ],
        color: { legend: true }
    });

    container.innerHTML = "";
    container.appendChild(us_plot);
    container.appendChild(d_plot);
}

window.addEventListener('resize', debounce(() => { plot(); }, 100));

updatePlot(plot);
setInterval(() => updatePlot(plot), 1000);
