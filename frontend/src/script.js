const API_BASE = "http://localhost:8000"; // Adjust if needed
const form = document.getElementById("route-form");
const addBtn = document.getElementById("add-waypoint-btn");
const waypointsDiv = document.getElementById("waypoints");
const listUl = document.getElementById("route");
const detalSection = document.getElementById("route-details");
const routeInfo = document.getElementById("route-info");

let waypointCount = 0;


function createWaypointInput() {
    waypointCount += 1;
    const div = document.createElement("div");
    div.className = "waypoint-input";
    div.innerHTML = `
        <label for="waypoint-${waypointCount}">Waypoint ${waypointCount}:</label>
        <input type="text" id="waypoint-${waypointCount}" name="waypoints" required>
        <button type="button" class="remove-waypoint-btn">Remove</button>
    `;
    waypointsDiv.appendChild(div);