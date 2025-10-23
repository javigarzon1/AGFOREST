const API_BASE = "http://localhost:8000"; // Adjustar según sea necesario
const form = document.getElementById("route-form");
const addBtn = document.getElementById("add-waypoint-btn");
const waypointsDiv = document.getElementById("waypoints");
const listUl = document.getElementById("route");
const detalSection = document.getElementById("route-details");
const routeInfo = document.getElementById("route-info");
const waypointList = document.getElementById("waypoint-list");
const closeDetailsBtn = document.getElementById("close-details-btn");

let waypointCount = 0;


function createWaypointInput() { // Función para crear un nuevo conjunto de inputs de waypoint
    const index = waypointCount;
    waypointCount += 1;
    const div = document.createElement("div");
    div.className = "waypoint";
    div.innerHTML = `
        <input type="number" step="0.0001" placeholder="Latitud" name="lat-${index}" required />
        <input type="number" step="0.0001" placeholder="Longitud" name="lng-${index}" required />
        <button type="button" class="remove-waypoint-btn">Remove</button>
    `;
    div.querySelector(".remove-waypoint-btn").addEventListener("click", () => div.remove());
    return div;
}
addBtn.addEventListener("click", () => { // Agregar nuevo waypoint al formulario
    waypointsDiv.appendChild(createWaypointInput());
});

form.addEventListener("submit", async (e) => { // Enviar formulario de nueva ruta
    e.preventDefault(); // Prevenir comportamiento por defecto
    const name = document.getElementById("route-name").value; // Obtener nombre de la ruta
    const waypoints = Array.from(waypointsDiv.querySelectorAll(".waypoint")).map((wp, i) => { // Recolectar datos de waypoints
        const lat = parseFloat(wp.querySelector(`input[name="lat-${i}"]`).value);
        const lng = parseFloat(wp.querySelector(`input[name="lng-${i}"]`).value);
        return { latitude: lat, longitude: lng, order: i + 1 };
    });

    const response = await fetch(`${API_BASE}/api/routes/`, { // Enviar datos al backend
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({name, waypoints}), // Incluir waypoints en el cuerpo de la solicitud 
    });
    if (response.ok) { // Manejar respuesta exitosa
        alert("¡Ruta creada satisfactoriamente!");
        form.reset();
        waypointsDiv.innerHTML = "";
        if (typeof loadRoutes === "function") loadRoutes();
    } else {
        alert("Error en la ruta.");
    }   
});
async function loadRoutes() { // Cargar y mostrar rutas existentes
    const response = await fetch(`${API_BASE}/api/routes/`);
    const routes = await response.json();
  routeInfo.textContent = `${route.name} — ${(route.distance_m / 1000).toFixed( 2 )} km`;
    waypointList.innerHTML = route.waypoints.map(wp => `<li>(${wp.latitude.toFixed(4)}, ${wp.longitude.toFixed(4)})</li>`).join("");
    detalSection.style.display = "block";
    }
    closeDetailsBtn.addEventListener("click", () => { // Cerrar sección de detalles
    detalSection.style.display = "none";
    });
    loadRoutes(); // Cargar rutas al iniciar la página