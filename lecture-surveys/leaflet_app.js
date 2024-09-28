var map = L.map('map').setView([48.1351, 11.5820], 11);

var customSvg = `<svg xmlns="http://www.w3.org/2000/svg" fill="tomato" viewBox="0 0 24 24" stroke-width="1.5" stroke="black" class="size-6"> <path stroke-linecap="round" stroke-linejoin="round" d="M4.26 10.147a60.438 60.438 0 0 0-.491 6.347A48.62 48.62 0 0 1 12 20.904a48.62 48.62 0 0 1 8.232-4.41 60.46 60.46 0 0 0-.491-6.347m-15.482 0a50.636 50.636 0 0 0-2.658-.813A59.906 59.906 0 0 1 12 3.493a59.903 59.903 0 0 1 10.399 5.84c-.896.248-1.783.52-2.658.814m-15.482 0A50.717 50.717 0 0 1 12 13.489a50.702 50.702 0 0 1 7.74-3.342M6.75 15a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm0 0v-3.675A55.378 55.378 0 0 1 12 8.443m-7.007 11.55A5.981 5.981 0 0 0 6.75 15.75v-1.5" /> </svg>`;

var starSvg = `<svg xmlns="http://www.w3.org/2000/svg" fill="gold" viewBox="0 0 24 24" stroke-width="1.5" stroke="black" class="size-6">
  <path stroke-linecap="round" stroke-linejoin="round" d="M11.48 3.499a.562.562 0 0 1 1.04 0l2.125 5.111a.563.563 0 0 0 .475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 0 0-.182.557l1.285 5.385a.562.562 0 0 1-.84.61l-4.725-2.885a.562.562 0 0 0-.586 0L6.982 20.54a.562.562 0 0 1-.84-.61l1.285-5.386a.562.562 0 0 0-.182-.557l-4.204-3.602a.562.562 0 0 1 .321-.988l5.518-.442a.563.563 0 0 0 .475-.345L11.48 3.5Z" />
</svg>`

var customIcon = L.divIcon({
    html: customSvg,          // Set the SVG as the HTML content of the icon
    iconSize: [18, 18],       // Set the size of the icon
    className: 'custom-marker', // Use the custom class to isolate styles
});

var starIcon = L.divIcon({
    html: starSvg,          // Set the SVG as the HTML content of the icon
    iconSize: [35, 35],       // Set the size of the icon
    className: 'custom-marker', // Use the custom class to isolate styles
});

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);


function updateMarkers() {
    fetch('data')
    .then(response => response.json())
    .then(data => {
        map.eachLayer(function (layer) {
            if (layer instanceof L.Marker) {
                map.removeLayer(layer);
            }
        });

        markers = [];

        data.forEach(point => {
            if (point.lat !== null && point.lon !== null) {
                var marker = L.marker([point.lat, point.lon], { icon: customIcon })
                marker.addTo(map);
                markers.push(marker);
            }
        });

        L.marker([48.14750111417741, 11.564421781799227], { icon: starIcon }).addTo(map)

        // var group = new L.featureGroup(markers); 
        // map.fitBounds(group.getBounds().pad(0.5));
    });
}

function updateStats() {
    fetch('stats')
    .then(response => response.json())
    .then(data => {
        document.getElementById("n").innerText = data.n;
        document.getElementById("meandist").innerText = data.meandist;
    });
}


updateMarkers();
updateStats();

setInterval(updateMarkers, 2500);
setInterval(updateStats, 2500);
