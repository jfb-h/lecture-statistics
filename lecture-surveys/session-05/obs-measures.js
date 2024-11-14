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

let answers_lage = [];
let answers_streuung = [];

function updateData(data) {
    answers_lage = data.filter((d) => d.measure == "lage");
    answers_streuung = data.filter((d) => d.measure == "streuung");
}

function plot() {
    const container = document.getElementById('results');
    const containerWidth = container.offsetWidth;
    const containerHeight = container.offsetHeight;

    const labels = new Map();
    labels.set("landuse", "1 Landnutzung")
    labels.set("trust", "2 Vertrauen")
    labels.set("temp", "3 Temperatur")

    const p1 = Plot.plot({
        width: containerWidth,
        height: containerHeight / 2,
        style: { fontSize: "16px" },
        marginLeft: 50,
        marginRight: 50,
        marginBottom: 50,
        marginTop: 50,


        marks: [
            Plot.barY(answers_lage, Plot.groupX({ y: "count" }, { x: "value", fx: "variable" })),
            Plot.ruleY([0])
        ],
        x: { label: null, domain: ["AM", "GM", "Median", "Mode"] },
        y: { label: "Häufigkeit", },
        fx: { label: null, }
    });

    const p2 = Plot.plot({
        width: containerWidth,
        height: containerHeight / 2,
        style: { fontSize: "16px" },
        marginLeft: 50,
        marginRight: 50,
        marginBottom: 50,
        marginTop: 50,


        marks: [
            Plot.barY(answers_streuung, Plot.groupX({ y: "count" }, { x: "value", fx: "variable" })),
            Plot.ruleY([0])
        ],
        x: { label: null, domain: ["SD", "MAD", "Dissens", "Entropie"] },
        y: { label: "Häufigkeit", },
        fx: { label: null, }
    });

    container.innerHTML = "";
    container.appendChild(p1);
    container.appendChild(p2);
}

window.addEventListener('resize', debounce(() => { plot(); }, 100));

updatePlot(plot);
setInterval(() => updatePlot(plot), 1000);
