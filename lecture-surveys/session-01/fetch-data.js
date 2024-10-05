let surveydata = [];

function debounce(func, delay) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), delay);
    };
}

function updateData(route) {
    fetch(route)
        .then(response => response.json())
        .then(data => {
            surveydata = data;
            console.log("data updated")
        })
        .catch(error => { console.error("Error fetching data:", error); });
}

setInterval(_ => updateData('data'), 2000);

