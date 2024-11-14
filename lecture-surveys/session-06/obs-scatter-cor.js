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

// adapt these to the data used in the plot
let vars = [];
function updateData(data) {
    vars = data;
}

function pearsonCorrelation(x, y) {
    if (x.length !== y.length) {
        throw new Error("Arrays müssen die gleiche Länge haben");
    }
    const n = x.length;
    // Mittelwerte berechnen
    const meanX = x.reduce((acc, val) => acc + val, 0) / n;
    const meanY = y.reduce((acc, val) => acc + val, 0) / n;
    // Variablen initialisieren
    let numerator = 0;
    let denominatorX = 0;
    let denominatorY = 0;

    for (let i = 0; i < n; i++) {
        const diffX = x[i] - meanX;
        const diffY = y[i] - meanY;
        numerator += diffX * diffY;
        denominatorX += diffX ** 2;
        denominatorY += diffY ** 2;
    }
    const denominator = Math.sqrt(denominatorX * denominatorY);
    if (denominator === 0) return 0;
    return numerator / denominator;
}

function spearmanRankCorrelation(x, y) {
    if (x.length !== y.length) {
        throw new Error("Arrays müssen die gleiche Länge haben");
    }
    const n = x.length;
    // Funktion, um Ränge zu berechnen
    const getRanks = (arr) => {
        const sorted = [...arr].map((val, index) => ({ val, index }));
        sorted.sort((a, b) => a.val - b.val);
        const ranks = Array(n);
        for (let i = 0; i < n; i++) {
            if (i > 0 && sorted[i].val === sorted[i - 1].val) {
                ranks[sorted[i].index] = ranks[sorted[i - 1].index];
            } else {
                ranks[sorted[i].index] = i + 1;
            }
        }
        return ranks;
    };
    const rankX = getRanks(x);
    const rankY = getRanks(y);
    // Differenzen der Ränge und deren Quadrate berechnen
    let sumD2 = 0;
    for (let i = 0; i < n; i++) {
        const d = rankX[i] - rankY[i];
        sumD2 += d ** 2;
    }
    const spearmanCoefficient = 1 - (6 * sumD2) / (n * (n ** 2 - 1));
    return spearmanCoefficient;
}

function createSummary(data) {
    const ftm = d3.format(".2f");
    const vra = data.map(d => d.vara);
    const vrb = data.map(d => d.varb);
    const pcor = pearsonCorrelation(vra, vrb)
    const scor = spearmanRankCorrelation(vra, vrb)
    return `Pearson: <strong>${ftm(pcor)}</strong><br>
            Spearman: <strong>${ftm(scor)}</strong><br>`
}



function scatter() {
    const containerScatter = document.getElementById('scatter');
    const containerScatterWidth = containerScatter.offsetWidth;
    const containerScatterHeight = containerScatter.offsetHeight;

    document.getElementById('c1').innerHTML = createSummary(vars);


    const plotScatter = Plot.plot({
        width: containerScatterWidth,
        height: containerScatterHeight,
        style: { fontSize: "16px" },
        marginLeft: 60,
        marginRight: 50,
        marginBottom: 50,
        marginTop: 50,
        inset: 20,

        marks: [
            Plot.dot(vars, { y: "vara", x: "varb" }),
            Plot.crosshair(vars, { y: "vara", x: "varb", color: "blue" }),
            isoline.checked ? Plot.link({ length: 1 }, { x1: 0, x2: 500, y1: 0, y2: 500, stroke: "black", strokeOpacity: 0.2 }) : [],
            regression.checked ? Plot.linearRegressionY(vars, { y: "vara", x: "varb", stroke: "blue" }) : []
        ],
        x: { label: "Variable b", domain: [0, 100] },
        y: { label: "Variable a", domain: [0, 100] },
    });

    containerScatter.innerHTML = "";
    containerScatter.appendChild(plotScatter);
}

const regression = document.getElementById('check-regression');
document.getElementById('check-regression')
    .addEventListener('change', () => { scatter(); });

const isoline = document.getElementById('check-isoline');
document.getElementById('check-isoline')
    .addEventListener('change', () => { scatter(); });

window.addEventListener('resize', debounce(() => { scatter(); }, 100));

updatePlot(scatter);
setInterval(_ => updatePlot(scatter), 1000);

