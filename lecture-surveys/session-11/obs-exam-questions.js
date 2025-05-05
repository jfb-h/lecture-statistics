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

function plot() {
    const container = document.getElementById('results');
    const containerWidth = container.offsetWidth;
    const containerHeight = container.offsetHeight;

    const n = 4; // number of facet columns
    const keys = Array.from(d3.union(answers.map((d) => d.variable)));
    const index = new Map(keys.map((key, i) => [key, i]));
    const fx = (key) => index.get(key) % n;
    const fy = (key) => Math.floor(index.get(key) / n);

    const p1 = Plot.plot({
        width: containerWidth,
        height: containerHeight,
        style: { fontSize: "16px" },
        marginLeft: 50,
        marginRight: 50,
        marginBottom: 50,
        marginTop: 50,

        marks: [
            Plot.barY(answers, Plot.groupX({ y: "count" }, {
                x: "value",
                fx: (d) => fx(d.variable),
                fy: (d) => fy(d.variable),
            })),
            Plot.ruleY([0]),
            Plot.text(keys, { fx, fy, frameAnchor: "top-left", dx: 6, dy: 6 }),
        ],
        x: { label: null, domain: ["1", "2", "3", "4", "5"] },
        y: { label: "Häufigkeit", insetTop: 25 },
        fx: { label: null, }
    });


    container.innerHTML = "";
    container.appendChild(p1);
}

window.addEventListener('resize', debounce(() => { plot(); }, 100));

updatePlot(plot);
setInterval(() => updatePlot(plot), 1000);
