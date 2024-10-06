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

// adapt this to data used in plot
let geodata = [];
function updateData(data) {
    geodata = data;
}


async function getNUTS0() {
    try {
        const response = await fetch('https://gisco-services.ec.europa.eu/distribution/v2/nuts/geojson/NUTS_BN_10M_2024_4326_LEVL_0.geojson');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching GeoJSON data:', error);
    }
}
async function getNUTS1() {
    try {
        const response = await fetch('https://gisco-services.ec.europa.eu/distribution/v2/nuts/geojson/NUTS_BN_10M_2024_4326_LEVL_1.geojson');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching GeoJSON data:', error);
    }
}

async function plot() {
    const nuts1 = await getNUTS1();
    const nuts0 = await getNUTS0();
    if (!(nuts1 && nuts0)) {
        console.error('No GeoJSON data available to plot');
        return;
    }

    const domain = d3.geoCircle().center([11, 51]).radius(4.4)();

    const container = document.getElementById('density-map');
    const containerWidth = container.offsetWidth;
    const containerHeight = container.offsetHeight;

    const plot = Plot.plot({
        width: containerWidth,
        height: containerHeight,
        style: { fontSize: "16px" },
        color: { scheme: "YlGnBu" },
        projection: { type: "equal-earth", domain: domain },
        marks: [
            Plot.density(geodata, {
                x: "lon_before",
                y: "lat_before",
                bandwidth: 20,
                // stroke: "density",
                fill: "density",
                fillOpacity: 0.05
            }),
            Plot.geo(nuts1, { strokeOpacity: 0.2 }),
            Plot.geo(nuts0),
            Plot.dot(geodata, { x: "lon_before", y: "lat_before", fill: "currentColor", r: 2 }),
            Plot.dot([{ x: 11.58, y: 48.13 }], { x: "x", y: "y", fill: "orange", r: 7, symbol: "star" }),
            Plot.graticule(),
        ],
    });

    container.innerHTML = "";
    container.appendChild(plot);
}

window.addEventListener('resize', debounce(() => { plot(); }, 100));


updatePlot(plot);
setInterval(_ => updatePlot(plot), 1000);

