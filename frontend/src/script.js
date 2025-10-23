const API_BASE = "http://localhost:8000"; // Adjust if needed
const form = document.getElementById("route-form");
const addBtn = document.getElementById("add-waypoint-btn");
const waypointsDiv = document.getElementById("waypoints");
const listUl = document.getElementById("route");
const detalSection = document.getElementById("route-details");
const routeInfo = document.getElementById("route-info");
const waypointList = document.getElementById("waypoint-list");
const closeDetailsBtn = document.getElementById("close-details-btn");

let waypointCount = 0;


function createWaypointInput(index) {
    waypointCount += 1;
    const div = document.createElement("div");
    div.className = "waypoint-input";
    div.innerHTML = `
        <input type="number" step="0.0001" placeholder="Latitud" name="lat-${index}" required />
        <input type="number" step="0.0001" placeholder="Longitud" name="lng-${index}" required />
        <button type="button" class="remove-waypoint-btn">Remove</button>
    `;
    div.querySelector(".remove").addEventListener("click", () => div.remove());
    return div;
}
addBtn.addEventListener("click", () => {
waypointsDiv.appendChild(createWaypointInput(waypointCount));});



form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const name = document.getElementById("route-name").value;
const waypoints = Array.from(waypointsDiv.querySelectorAll(".waypoint")).map((wp, i) => {
    const lat = parseFloat(wp.querySelector(`input[name="lat-${i}"]`).value);
    const lng = parseFloat(wp.querySelector(`input[name="lng-${i}"]`).value);
    return { latitude: lat, longitude: lng, order: i + 1 };
});
    const response = await fetch(`${API_BASE}/api/routes/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({name, waypoints}),
    });
    if (response.ok) {
        alert("¡Ruta creada satisfactoriamente!");
        form.reset();
        waypointsDiv.innerHTML = "";
        loadRoutes();
    } else {
        alert("Error en la ruta.");
    }   
});
