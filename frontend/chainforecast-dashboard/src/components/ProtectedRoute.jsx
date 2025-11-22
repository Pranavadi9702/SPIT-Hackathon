// src/components/ProtectedRoute.jsx
import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function ProtectedRoute() {
  const { user, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-950">
        <div className="text-xs text-slate-400">Checking access...</div>
      </div>
    );
  }

  if (!user) {
    // Not logged in -> go to login, remember where they came from
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  // User is logged in -> render children routes (with DashboardLayout)
  return <Outlet />;
}

export default ProtectedRoute;
