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

    const n = 3; // number of facet columns
    const keys = Array.from(d3.union(answers.map((d) => d.variable)));
    const index = new Map(keys.map((key, i) => [key, i]));
    const fx = (key) => index.get(key) % n;
    const fy = (key) => Math.floor(index.get(key) / n);

    const labels = new Map();
    labels.set("bip", "Das deutsche BIP")
    labels.set("co2", "CO₂-Konzentration")
    labels.set("stars", "Sterne bei Amazon")
    labels.set("likes", "Youtube Likes")
    labels.set("shf", "Frauenanteil")
    labels.set("gen", "Generationszugehörigkeit")

    const p = Plot.plot({
        width: containerWidth,
        height: containerHeight,
        style: { fontSize: "16px" },
        marginLeft: 50,
        marginRight: 50,
        marginBottom: 50,
        marginTop: 50,


        marks: [
            Plot.barY(answers, Plot.groupX({ y: "count" }, { x: "value", fx: (d) => fx(d.variable), fy: (d) => fy(d.variable) })),
            Plot.text(keys, { fx, fy, text: (k) => labels.get(k), frameAnchor: "top-left", dx: 6, dy: -10 }),
            Plot.axisFx({ color: "white" }),
            Plot.axisFy({ color: "white" }),
            Plot.ruleY([0])
        ],
        x: { label: null, domain: ["num-dis", "num-kon", "kat-nom", "kat-ord"] },
        y: { label: "Häufigkeit", insetTop: 20 },
        facet: { label: null },
    });

    container.innerHTML = "";
    container.appendChild(p);
}

window.addEventListener('resize', debounce(() => { plot(); }, 100));

updatePlot(plot);
setInterval(() => updatePlot(plot), 1000);
