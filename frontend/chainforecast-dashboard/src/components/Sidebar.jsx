import { NavLink } from "react-router-dom";
import {
  Squares2X2Icon,
  ChartBarIcon,
  UsersIcon,
  TagIcon,
  Cog6ToothIcon,
} from "@heroicons/react/24/outline";

const menuItems = [
  { to: "/overview", label: "Overview", icon: Squares2X2Icon },
  { to: "/sales-forecast", label: "Sales Forecast", icon: ChartBarIcon },
  { to: "/customer-segmentation", label: "Customer Segmentation", icon: UsersIcon },
  { to: "/offers", label: "Offers", icon: TagIcon },
  { to: "/settings", label: "Settings", icon: Cog6ToothIcon },
];

function Sidebar() {
  return (
    <aside className="hidden md:flex md:flex-col w-64 bg-white/95 dark:bg-slate-950 text-slate-900 dark:text-slate-100 border-r border-slate-200 dark:border-slate-800">
      {/* Logo / brand */}
      <div className="flex items-center gap-2 px-6 py-4 border-b border-slate-200 dark:border-slate-800">
        <div className="h-9 w-9 rounded-xl bg-brand-500 flex items-center justify-center text-white font-semibold shadow-sm">
          CF
        </div>
        <div>
          <div className="font-semibold tracking-tight">ChainForecast</div>
          <div className="text-xs text-slate-500 dark:text-slate-400">
            AI Sales Forecast &amp; CRM
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-1">
        {menuItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2 rounded-xl text-sm font-medium transition
                ${
                  isActive
                    ? "bg-slate-900 text-slate-100 shadow-sm dark:bg-slate-800"
                    : "text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800/70"
                }`
              }
            >
              <Icon className="h-5 w-5" />
              {item.label}
            </NavLink>
          );
        })}
      </nav>
    </aside>
  );
}

export default Sidebar;