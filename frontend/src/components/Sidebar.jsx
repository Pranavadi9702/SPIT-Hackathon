// src/components/Sidebar.jsx
import { NavLink, useNavigate } from "react-router-dom";
import {
  Squares2X2Icon,
  ChartBarIcon,
  UsersIcon,
  TagIcon,
  Cog6ToothIcon,
  ArrowRightOnRectangleIcon,
} from "@heroicons/react/24/outline";

// 🔽 ADD THESE IMPORTS
import { signOut } from "firebase/auth";
import { auth } from "../firebase"; // make sure this path matches your firebase.js

const menuItems = [
  { to: "/overview", label: "Overview", icon: Squares2X2Icon },
  { to: "/sales-forecast", label: "Sales Forecast", icon: ChartBarIcon },
  { to: "/customer-segmentation", label: "Customer Segmentation", icon: UsersIcon },
  { to: "/offers", label: "Offers", icon: TagIcon },
  { to: "/settings", label: "Settings", icon: Cog6ToothIcon },
];

function Sidebar() {
  const navigate = useNavigate();

  // 🔽 PROPER LOGOUT HANDLER
  const handleLogout = async () => {
    try {
      await signOut(auth);              // 1. Clear Firebase auth session
      navigate("/login", { replace: true }); // 2. Go to login page
    } catch (err) {
      console.error("Logout error:", err);
      // optional: show a toast or alert here
    }
  };

  return (
    <aside className="hidden md:flex md:flex-col w-60 bg-slate-900 text-slate-100">
      <div className="h-16 flex items-center px-4 border-b border-slate-800">
        <div className="h-9 w-9 rounded-2xl bg-gradient-to-br from-brand-500 to-brand-700 flex items-center justify-center text-xs font-semibold">
          CF
        </div>
        <div className="ml-2">
          <div className="text-xs font-semibold">ChainForecast</div>
          <div className="text-[10px] text-slate-400">Sales AI Dashboard</div>
        </div>
      </div>

      <nav className="flex-1 mt-4">
        <div className="px-3 mb-2 text-[10px] uppercase tracking-wide text-slate-500">
          Main
        </div>
        <ul className="space-y-1 px-2">
          {menuItems.map((item) => {
            const Icon = item.icon;
            return (
              <li key={item.to}>
                <NavLink
                  to={item.to}
                  className={({ isActive }) =>
                    [
                      "flex items-center gap-3 px-3 py-2 rounded-xl text-sm font-medium transition",
                      isActive
                        ? "bg-slate-800 text-white"
                        : "text-slate-300 hover:bg-slate-800/70 hover:text-white",
                    ].join(" ")
                  }
                >
                  <Icon className="h-5 w-5" />
                  <span>{item.label}</span>
                </NavLink>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* 🔽 USE THE NEW HANDLER */}
      <button
        onClick={handleLogout}
        className="m-3 flex items-center gap-2 px-3 py-2 rounded-xl text-sm font-medium text-slate-300 hover:bg-slate-800/80"
      >
        <ArrowRightOnRectangleIcon className="h-5 w-5" />
        Logout
      </button>
    </aside>
  );
}

export default Sidebar;
