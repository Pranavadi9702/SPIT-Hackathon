// src/api/backend.js
const API_BASE = "http://127.0.0.1:5000";

async function handleResponse(res) {
  if (!res.ok) {
    throw new Error(`HTTP ${res.status}`);
  }
  const data = await res.json();
  if (data.status && data.status !== "success") {
    throw new Error(data.message || "Backend error");
  }
  return data;
}

export async function fetchForecastSummary() {
  const res = await fetch(`${API_BASE}/api/forecast-summary`);
  return handleResponse(res);
}

export async function fetchSegmentsSummary() {
  const res = await fetch(`${API_BASE}/api/segments-summary`);
  return handleResponse(res);
}
