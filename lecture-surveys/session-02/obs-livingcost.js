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
    answers = data.filter((d) => d.wohnsituation != "Andere" && d.kosten < 10000 && d.wohnsituation != null);
}

const groups = new Map();
groups.set("Alleine", "c1");
groups.set("Familie", "c2");
groups.set("WG", "c3");

function createSummary(data) {
    const fmt = d3.format(".1f");
    const cost = data.map(d => d.kosten);
    const sum = d3.sum(cost);
    const mean = d3.mean(cost);
    return `Anzahl: <strong>${data.length}</strong><br>
            Summe: <strong>${fmt(sum)}</strong><br>
            Mittelwert: <strong>${fmt(mean)}</strong>`
}

function plot() {
    const container = document.getElementById('wohnsituation');
    const containerWidth = container.offsetWidth;
    const containerHeight = container.offsetHeight;

    ["Alleine", "Familie", "WG"].forEach((g) => {
        const data = answers.filter((d) => d.wohnsituation == g);
        document.getElementById(groups.get(g)).innerHTML = createSummary(data);
    });

    const p = Plot.plot({
        width: containerWidth,
        height: containerHeight,
        style: { fontSize: "16px" },
        marginLeft: 50,
        marginRight: 150,
        marginBottom: 50,
        marginTop: 50,
        facet: { data: answers, y: "wohnsituation" },

        marks: [
            Plot.rectY(answers, Plot.binX({ y: "proportion-facet" }, { x: "kosten" })),
            Plot.ruleX(answers, Plot.groupZ({ x: "mean" }, { x: "kosten", stroke: "red", strokeWidth: 5 })),
            Plot.ruleY([0])
        ],
        x: { label: "Wohnkosten (Euro)" },
        y: { label: "Rel. Häufigkeit (%)", percent: true },
        fy: { label: null },
    });

    container.innerHTML = "";
    container.appendChild(p);
}

window.addEventListener('resize', debounce(() => { plot(); }, 100));

updatePlot(plot);
setInterval(() => updatePlot(plot), 1000);
