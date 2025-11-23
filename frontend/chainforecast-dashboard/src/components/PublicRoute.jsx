// src/components/PublicRoute.jsx
import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function PublicRoute({ children }) {
  const { user, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-950">
        <div className="text-xs text-slate-400">Loading...</div>
      </div>
    );
  }

  // If already logged in, send to overview
  if (user) {
    return (
      <Navigate
        to="/overview"
        replace
        state={location.state?.from ? { from: location.state.from } : {}}
      />
    );
  }

  // Not logged in -> show the login/signup page
  return children;
}

export default PublicRoute;
