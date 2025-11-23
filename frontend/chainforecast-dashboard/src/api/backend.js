// src/api/backend.js
const API_BASE = "http://127.0.0.1:5000";

async function handleResponse(res) {
  // NOTE: For auth APIs we always return HTTP 200,
  // and use { status: "success" | "error" } in JSON.
  if (!res.ok) {
    throw new Error(`HTTP ${res.status}`);
  }
  const data = await res.json();
  if (data.status && data.status !== "success") {
    throw new Error(data.message || "Backend error");
  }
  return data;
}

// ==== JWT helpers (frontend) ====
function getAuthToken() {
  if (typeof window === "undefined") return null;
  return (
    window.localStorage.getItem("cf_jwt") ||
    window.sessionStorage.getItem("cf_jwt")
  );
}

function getAuthHeaders() {
  const token = getAuthToken();
  if (!token) return {};
  return {
    Authorization: `Bearer ${token}`,
  };
}

// ==== Existing APIs ====
export async function fetchForecastSummary() {
  const res = await fetch(`${API_BASE}/api/forecast-summary`, {
    headers: {
      ...getAuthHeaders(),
    },
  });
  return handleResponse(res);
}

export async function fetchSegmentsSummary() {
  const res = await fetch(`${API_BASE}/api/segments-summary`, {
    headers: {
      ...getAuthHeaders(),
    },
  });
  return handleResponse(res);
}

// ==== NEW: Auth APIs for email/password (JWT-based) ====

export async function signupWithEmail(name, email, password) {
  const res = await fetch(`${API_BASE}/api/auth/signup`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ name, email, password }),
  });
  return handleResponse(res);
}

export async function loginWithEmail(email, password) {
  const res = await fetch(`${API_BASE}/api/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });
  return handleResponse(res);
}
