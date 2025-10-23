const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export async function createRoute(data) {
  const response = await fetch(`${API_BASE} api/routes/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  return response.json();
}
export async function getRoute(id) {
  const response = await fetch(`${API_BASE} api/routes/${id}/`);
  return response.json();
}

export async function listRoutes() {
  const response = await fetch(`${API_BASE} api/routes/`);
  return response.json();
}