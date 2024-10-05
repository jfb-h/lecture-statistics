var customSvg = `<svg xmlns="http://www.w3.org/2000/svg" fill="tomato" viewBox="0 0 24 24" stroke-width="1.5" stroke="black" class="size-6"> <path stroke-linecap="round" stroke-linejoin="round" d="M4.26 10.147a60.438 60.438 0 0 0-.491 6.347A48.62 48.62 0 0 1 12 20.904a48.62 48.62 0 0 1 8.232-4.41 60.46 60.46 0 0 0-.491-6.347m-15.482 0a50.636 50.636 0 0 0-2.658-.813A59.906 59.906 0 0 1 12 3.493a59.903 59.903 0 0 1 10.399 5.84c-.896.248-1.783.52-2.658.814m-15.482 0A50.717 50.717 0 0 1 12 13.489a50.702 50.702 0 0 1 7.74-3.342M6.75 15a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm0 0v-3.675A55.378 55.378 0 0 1 12 8.443m-7.007 11.55A5.981 5.981 0 0 0 6.75 15.75v-1.5" /> </svg>`;

var starSvg = `<svg xmlns="http://www.w3.org/2000/svg" fill="gold" viewBox="0 0 24 24" stroke-width="1.5" stroke="black" class="size-6">
  <path stroke-linecap="round" stroke-linejoin="round" d="M11.48 3.499a.562.562 0 0 1 1.04 0l2.125 5.111a.563.563 0 0 0 .475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 0 0-.182.557l1.285 5.385a.562.562 0 0 1-.84.61l-4.725-2.885a.562.562 0 0 0-.586 0L6.982 20.54a.562.562 0 0 1-.84-.61l1.285-5.386a.562.562 0 0 0-.182-.557l-4.204-3.602a.562.562 0 0 1 .321-.988l5.518-.442a.563.563 0 0 0 .475-.345L11.48 3.5Z" />
</svg>`

var customIcon = L.divIcon({
    html: customSvg,
    className: 'custom-marker',
    iconSize: [14, 14],
    iconAnchor: [7, 7]
});

var starIcon = L.divIcon({
    html: starSvg,
    className: 'custom-marker',
    iconSize: [24, 24],
    iconAnchor: [12, 12]
});

var map_current = L.map('map-current').setView([48.1351, 11.5820], 10);
var map_before = L.map('map-before').setView([51.545483, 9.905548], 6);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map_current);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map_before);

L.marker([48.147667, 11.56451], { icon: starIcon }).addTo(map_current);
L.marker([48.147667, 11.56451], { icon: starIcon }).addTo(map_before);

var n_old = 0;
var counter_current = 0;
var counter_before = 0;

function updateMarkers(route) {
    fetch(route)
        .then(response => response.json())
        .then(data => {
            var n_new = data.length;

            if (n_new == n_old) {
                console.log("No data changes");
                return;
            }

            data.slice(n_old).forEach(point => {
                if (point.lat_current !== null && point.lon_current !== null) {
                    var marker_current = L.marker([point.lat_current, point.lon_current], { icon: customIcon })
                    marker_current.addTo(map_current);
                    counter_current += 1;
                }
                if (point.lat_before !== null && point.lon_before !== null) {
                    var marker_before = L.marker([point.lat_before, point.lon_before], { icon: customIcon })
                    marker_before.addTo(map_before);
                    counter_before += 1;
                }
            });

            document.getElementById("n-map-current").innerText = " (n = " + counter_current + ")";
            document.getElementById("n-map-before").innerText = " (n = " + counter_before + ")";

            n_old = n_new;
        })
        .catch(error => { console.error("Error fetching data:", error); });
}

updateMarkers('data');
setInterval(_ => updateMarkers('data'), 1000);
