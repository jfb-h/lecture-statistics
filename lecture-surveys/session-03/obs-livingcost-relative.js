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
    answers = data
        .filter((d) => d.wohnsituation != "Andere" && d.kosten < 10000 && d.wohnsituation != null)
        .map((d) => {
            return {
                wohnsituation: d.wohnsituation,
                kosten: d.kosten / 538 * 100 // Wohnung in HD 
            }
        });
}

const groups = new Map();
groups.set("Alleine", "c1-gm");
groups.set("Familie", "c2-gm");
groups.set("WG", "c3-gm");

function geometricMean(data) {
    return Math.exp(d3.mean(data.map((d) => Math.log(d || NaN))))
}

function createSummary(data) {
    const fmt = d3.format(".1f");
    const cost = data.map(d => d.kosten);
    const am = d3.mean(cost);
    const gm = geometricMean(cost);
    return `Anzahl: <strong>${data.length}</strong><br>
            <span style="color:red">AM</span>: <strong>${fmt(am)}</strong><br>
            <span style="color:blue">GM</span>: <strong>${fmt(gm)}</strong>`
}

function plot() {
    const container = document.getElementById('wohnsituation-gm');
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
            Plot.ruleX(answers, Plot.groupZ({ x: geometricMean }, { x: "kosten", stroke: "blue", strokeWidth: 5 })),
            Plot.ruleX(answers, Plot.groupZ({ x: "mean" }, { x: "kosten", fy: "wohnsituation", stroke: "red", strokeWidth: 5 })),
            Plot.ruleY([0]),
            Plot.ruleX([100])
        ],
        x: { label: "Relative Wohnkosten (% HD)" },
        y: { label: "Rel. Häufigkeit (%)", percent: true },
        fy: { label: null },
    });

    container.innerHTML = "";
    container.appendChild(p);
}

window.addEventListener('resize', debounce(() => { plot(); }, 100));

updatePlot(plot);
setInterval(() => updatePlot(plot), 1000);
