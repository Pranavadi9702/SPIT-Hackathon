// src/components/ProtectedRoute.jsx
import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

// Read JWT user from storage (used by email/password login)
function getJwtUser() {
  if (typeof window === "undefined") return null;
  try {
    const stored =
      window.localStorage.getItem("cf_user") ||
      window.sessionStorage.getItem("cf_user");
    if (!stored) return null;
    return JSON.parse(stored);
  } catch {
    return null;
  }
}

// Check if a JWT token exists
function hasJwtToken() {
  if (typeof window === "undefined") return false;
  const token =
    window.localStorage.getItem("cf_jwt") ||
    window.sessionStorage.getItem("cf_jwt");
  return !!token;
}

function ProtectedRoute() {
  const { user, loading } = useAuth();
  const location = useLocation();

  // While Firebase auth / context is still resolving
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-950">
        <div className="text-xs text-slate-400">Checking access...</div>
      </div>
    );
  }

  // Context user (Firebase / your AuthContext)
  const contextUser = user;

  // JWT user (email/password login from backend)
  const jwtUser = getJwtUser();
  const jwtPresent = hasJwtToken();

  const isAuthenticated = !!contextUser || (jwtPresent && !!jwtUser);

  if (!isAuthenticated) {
    // Not logged in -> go to login, remember where they came from
    return (
      <Navigate
        to="/login"
        replace
        state={{ from: location }}
      />
    );
  }

  // User is logged in -> render children routes (with DashboardLayout)
  return <Outlet />;
}

export default ProtectedRoute;
