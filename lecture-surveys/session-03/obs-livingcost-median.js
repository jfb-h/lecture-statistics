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
    answers = data.filter((d) => d.wohnsituation != "Andere")
}

function plot() {
    const container = document.getElementById('wohnsituation-median');
    const containerWidth = container.offsetWidth;
    const containerHeight = container.offsetHeight;

    const cost = answers.map((d) => d.kosten);
    const mean = Math.log10(d3.mean(cost) || NaN);
    const mean_no = Math.log10(d3.mean(cost.filter((d) => d < 10000)) || NaN);

    const p = Plot.plot({
        width: containerWidth,
        height: containerHeight,
        style: { fontSize: "16px" },
        marginLeft: 30,
        marginRight: 30,
        marginBottom: 50,
        marginTop: 50,

        marks: [
            Plot.rectY(answers, Plot.binX({ y: "count" }, { x: (d) => Math.log10(d.kosten || NaN) })),
            Plot.ruleX([mean], { stroke: "red", strokeWidth: 5 }),
            Plot.ruleX([mean_no], { stroke: "blue", strokeWidth: 5 }),
            Plot.ruleY([0])
        ],
        x: { label: "Kosten (€)", type: "log", transform: (d) => Math.pow(10, d) },
        y: { label: "Häufigkeit" },
        color: { legend: true },
    });

    container.innerHTML = "";
    container.appendChild(p);
}

window.addEventListener('resize', debounce(() => { plot(); }, 100));

updatePlot(plot);
setInterval(() => updatePlot(plot), 1000);
