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

// adapt this to data
const parser = d3.timeParse("%H:%M");

let getuptimes = [];
function updateData(data) {
    getuptimes = data.map(d => parser(d.time));
}

function hist() {
    const container = document.getElementById('hist-getuptime');
    const containerWidth = container.offsetWidth;
    const containerHeight = container.offsetHeight;

    const histogram = Plot.plot({
        width: containerWidth,
        height: containerHeight,
        style: {fontSize: "16px"},
        marginLeft: 50,
        marginRight: 50,
        marginBottom: 50,
        marginTop: 50,

        marks: [
            Plot.rectY(getuptimes, Plot.binX({y: "count"}, {
                x: d => d, 
                thresholds: d3.utcMinute.every(15) 
            })),
            Plot.ruleY([0])
        ],
        x: {
            label: "Uhrzeit",
            tickFormat: d3.utcFormat("%H:%M"),
        },
        y: {
            label: "Häufigkeit",
        },
    });

    container.innerHTML = "";
    container.appendChild(histogram);
}

window.addEventListener('resize', debounce(() => { hist(); }, 100));

updatePlot(hist);
setInterval(x => updatePlot(hist), 1000);
