import { Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Overview from "./pages/Overview";
import SalesForecast from "./pages/SalesForecast";
import CustomerSegmentation from "./pages/CustomerSegmentation";
import Offers from "./pages/Offers";
import Settings from "./pages/Settings";
import DashboardLayout from "./layouts/DashboardLayout";

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />

      <Route element={<DashboardLayout />}>
        <Route index element={<Navigate to="/overview" replace />} />
        <Route path="/overview" element={<Overview />} />
        <Route path="/sales-forecast" element={<SalesForecast />} />
        <Route path="/customer-segmentation" element={<CustomerSegmentation />} />
        <Route path="/offers" element={<Offers />} />
        <Route path="/settings" element={<Settings />} />
      </Route>

      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
}

export default App;
