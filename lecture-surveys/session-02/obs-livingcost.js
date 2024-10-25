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
    
    const valueAllein = document.getElementById('c1');
    const valueFamilie = document.getElementById('c2');
    const valueWG = document.getElementById('c3');

    const dataAlleine = answers.filter((d) => d.wohnsituation == "Alleine");
    const textAlleine = "<em>Anzahl (n):</em> " + dataAlleine.length + "<br>" +
                        "<em>Summe:</em> " + d3.sum(dataAlleine.map((d) => d.kosten))+ "<br>" +
                        "<em>Mittelwert:</em> " + Math.round(d3.mean(dataAlleine.map((d) => d.kosten))*100) / 100;

    const dataFamilie = answers.filter((d) => d.wohnsituation == "Familie");
    const textFamilie = "<em>Anzahl (n):</em> " + dataFamilie.length + "<br>" +
                        "<em>Summe:</em> " + d3.sum(dataFamilie.map((d) => d.kosten))+ "<br>" +
                        "<em>Mittelwert:</em> " + Math.round(d3.mean(dataFamilie.map((d) => d.kosten))*100) / 100;

    const dataWG = answers.filter((d) => d.wohnsituation == "WG");
    const textWG = "<em>Anzahl (n):</em> " + dataWG.length + "<br>" +
                        "<em>Summe:</em> " + d3.sum(dataWG.map((d) => d.kosten))+ "<br>" +
                        "<em>Mittelwert:</em> " + Math.round(d3.mean(dataWG.map((d) => d.kosten))*100) / 100;
    
    valueAllein.innerHTML = textAlleine;
    valueFamilie.innerHTML = textFamilie;
    valueWG.innerHTML = textWG;


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
            Plot.ruleX(answers, Plot.groupZ({ x: "mean" }, { x: "kosten", fy: "wohnsituation", stroke: "red", strokeWidth: 5 })),
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
