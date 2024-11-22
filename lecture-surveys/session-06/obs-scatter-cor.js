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
    const meanX = d3.mean(x);
    const meanY = d3.mean(x);

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
    const n = x.length;
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
    let sumD2 = 0;
    for (let i = 0; i < n; i++) {
        const d = rankX[i] - rankY[i];
        sumD2 += d ** 2;
    }
    const spearmanCoefficient = 1 - (6 * sumD2) / (n * (n ** 2 - 1));
    return spearmanCoefficient;
}


function scatter() {
    const containerScatter = document.getElementById('scatter');
    const containerScatterWidth = containerScatter.offsetWidth;
    const containerScatterHeight = containerScatter.offsetHeight;

    const x = vars.map(d => d.vara);
    const y = vars.map(d => d.varb);

    const pcor = pearsonCorrelation(x, y)
    const scor = spearmanRankCorrelation(x, y)

    const meanX = d3.mean(x);
    const meanY = d3.mean(y);

    const fmt = d3.format(".2f");

    const summaryCorr = `<strong>${fmt(pcor)}</strong><br>`
    const summaryRank = `<strong>${fmt(scor)}</strong><br>`
    const summaryMeans = `Körpergröße: <strong>${fmt(meanX)}</strong><br>
                          Schuhgröße: <strong>${fmt(meanY)}</strong><br>`

    document.getElementById('c1').innerHTML = summaryMeans;
    document.getElementById('c2').innerHTML = summaryCorr;
    document.getElementById('c3').innerHTML = summaryRank;

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
        ],
        x: { label: "Schuhgroesse", domain: [30, 60] },
        y: { label: "Koerpergroesse", domain: [100, 250] },
    });

    containerScatter.innerHTML = "";
    containerScatter.appendChild(plotScatter);
}

window.addEventListener('resize', debounce(() => { scatter(); }, 100));

updatePlot(scatter);
setInterval(_ => updatePlot(scatter), 1000);

