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
    const plot1Container = document.getElementById("plot1");
    const plot2Container = document.getElementById("plot2");
    const plot3Container = document.getElementById("plot3");


    const containerWidth = 1000;
    const containerHeight = 1000;



    const p1 = Plot.plot({
        width: containerWidth,
        height: containerHeight / 2,
        style: { fontSize: "16px" },
        marginLeft: 50,
        marginRight: 50,
        marginBottom: 50,
        marginTop: 50,
        
        y: {
            grid: true,
            percent: true
          },

        x: {
            label: "1. Zahl",
            domain: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
                40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50], 
            tickRotate: 90,
            labelFontSize: 8,
        },

        marks: [
            Plot.barY(answers,
                Plot.groupX({
              y:
              "count"
                  }, {
              x:
              "vara"}))
        ],

        
    });

    const p2 = Plot.plot({
        width: containerWidth,
        height: containerHeight / 2,
        style: { fontSize: "16px" },
        marginLeft: 50,
        marginRight: 50,
        marginBottom: 50,
        marginTop: 50,

        y: {
            grid: true,
            percent: true
          },

        x: {
            label: "2. Zahl",
            domain: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
                40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50], 
            tickRotate: 90,
            labelFontSize: 8,
        },

        marks: [
            Plot.barY(answers,
                Plot.groupX({
              y:
              "count"
                  }, {
              x:
              "varb"}))
        ],  
    });

    const answersWithSum = answers.map(d => ({
        ...d,
        sum: d.vara + d.varb // Add a new field for the sum
    }));

    const p3 = Plot.plot({
        width: containerWidth*2,
        height: containerHeight / 2,
        style: { fontSize: "16px" },
        marginLeft: 50,
        marginRight: 50,
        marginBottom: 50,
        marginTop: 50,
    
        y: {
            grid: true,
            percent: true
        },
    
        x: {
            label: "Summe",
            domain: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
                40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59,
                60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79,
                80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100], 
            tickRotate: 90,
            labelFontSize: 5,
        },
    
        marks: [
            Plot.barY(
                answersWithSum,
                Plot.groupX(
                    { y: "count" }, // Count occurrences for each sum
                    { x: "sum" }    // Use the sum as the x-axis
                )
            )
        ]
    });

    plot1Container.innerHTML = "";
    plot2Container.innerHTML = "";
    plot3Container.innerHTML = "";
    plot1Container.appendChild(p1);
    plot2Container.appendChild(p2);
    plot3Container.appendChild(p3);
}

window.addEventListener('resize', debounce(() => { plot(); }, 100));

updatePlot(plot);
setInterval(() => updatePlot(plot), 1000);
