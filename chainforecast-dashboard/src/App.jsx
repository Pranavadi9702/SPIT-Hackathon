import { useEffect, useState } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Overview from "./pages/Overview";
import SalesForecast from "./pages/SalesForecast";
import CustomerSegmentation from "./pages/CustomerSegmentation";
import Offers from "./pages/Offers";
import Settings from "./pages/Settings";
import DashboardLayout from "./layouts/DashboardLayout";

function App() {
  // theme state: "light" | "dark", persisted in localStorage
  const [theme, setTheme] = useState(
    () => localStorage.getItem("theme") || "light"
  );

  // apply theme to <html> and save
  useEffect(() => {
    const root = window.document.documentElement;
    if (theme === "dark") {
      root.classList.add("dark");
    } else {
      root.classList.remove("dark");
    }
    localStorage.setItem("theme", theme);
  }, [theme]);

  const toggleTheme = () =>
    setTheme((prev) => (prev === "dark" ? "light" : "dark"));

  return (
    <Routes>
      <Route path="/login" element={<Login />} />

      {/* Pass theme + toggle into dashboard layout */}
      <Route
        element={
          <DashboardLayout theme={theme} toggleTheme={toggleTheme} />
        }
      >
        <Route index element={<Navigate to="/overview" replace />} />
        <Route path="/overview" element={<Overview />} />
        <Route path="/sales-forecast" element={<SalesForecast />} />
        <Route
          path="/customer-segmentation"
          element={<CustomerSegmentation />}
        />
        <Route path="/offers" element={<Offers />} />
        <Route path="/settings" element={<Settings />} />
      </Route>

      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
}

export default App;
