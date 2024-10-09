import * as Plot from "https://cdn.jsdelivr.net/npm/@observablehq/plot@0.6/+esm";

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

// adapt this to data used in plot
let gradedata = [];
function updateData(data) {
    gradedata = data;
}

function boxplot() {
    const container = document.getElementById('boxplot-grade');
    const containerWidth = container.offsetWidth;
    const containerHeight = container.offsetHeight;

    const boxplot = Plot.plot({
        width: containerWidth,
        height: containerHeight,
        style: { fontSize: "16px" },
        marginLeft: 170,
        marginRight: 50,
        marginBottom: 50,
        marginTop: 50,

        marks: [
            boxordot.checked ?
                Plot.dot(gradedata, Plot.dodgeY("middle", { fy: "minor", x: "grade" }),) :
                Plot.boxX(gradedata, { x: "grade", fy: "minor" }),
        ],
        x: { label: "Punkte", grid: true, domain: [0, 15] },
        y: { label: null, },
        fy: { label: null, },
    });

    container.innerHTML = "";
    container.appendChild(boxplot);
}

window.addEventListener('resize', debounce(() => { boxplot(); }, 100));

const boxordot = document.getElementById('check-boxordot');
document.getElementById('check-boxordot')
    .addEventListener('change', () => { boxplot(); });

updatePlot(boxplot);
setInterval(_ => updatePlot(boxplot), 1000);

