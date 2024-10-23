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
    answers = data.filter((d) => d.wohnsituation != "Andere");
}

function plot() {
    const container = document.getElementById('wohnsituation');
    const containerWidth = container.offsetWidth;
    const containerHeight = container.offsetHeight;

    const p = Plot.plot({
        width: containerWidth,
        height: containerHeight,
        style: { fontSize: "16px" },
        marginLeft: 50,
        marginRight: 150,
        marginBottom: 50,
        marginTop: 50,

        marks: [
            Plot.rectY(answers, Plot.binX({ y: "count" }, { x: "kosten", fy: "wohnsituation" })),
            Plot.ruleX(answers, Plot.groupZ({ x: "mean" }, { x: "kosten", fy: "wohnsituation", stroke: "red", strokeWidth: 4 })),
            Plot.ruleY([0])
        ],
        x: { label: null },
        y: { label: "Häufigkeit" },
        fy: { label: null },
    });

    container.innerHTML = "";
    container.appendChild(p);
}

window.addEventListener('resize', debounce(() => { plot(); }, 100));

updatePlot(plot);
setInterval(() => updatePlot(plot), 1000);
