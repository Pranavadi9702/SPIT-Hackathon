import { useLocation } from "react-router-dom";
import { BellIcon, ChevronDownIcon, MagnifyingGlassIcon } from "@heroicons/react/24/outline";

const titleMap = {
  "/overview": "Overview",
  "/sales-forecast": "Sales Forecast",
  "/customer-segmentation": "Customer Segmentation",
  "/offers": "Offers",
  "/settings": "Settings",
};

function Header() {
  const location = useLocation();
  const title = titleMap[location.pathname] || "Dashboard";

  return (
    <header className="h-16 border-b border-slate-200 bg-white/80 backdrop-blur flex items-center justify-between px-4 sm:px-6 lg:px-8">
      <h1 className="text-lg sm:text-xl font-semibold tracking-tight text-slate-900">
        {title}
      </h1>

      <div className="flex items-center gap-3">
        <div className="hidden sm:flex items-center bg-slate-100 rounded-full px-3 py-1.5">
          <MagnifyingGlassIcon className="h-4 w-4 text-slate-400" />
          <input
            type="text"
            placeholder="Search in ChainForecast..."
            className="bg-transparent border-none focus:outline-none text-sm px-2 w-40 lg:w-56"
          />
        </div>

        <button className="relative p-2 rounded-full hover:bg-slate-100">
          <BellIcon className="h-5 w-5 text-slate-500" />
          <span className="absolute top-1 right-1 inline-flex h-2 w-2 rounded-full bg-red-500" />
        </button>

        <button className="flex items-center gap-2 rounded-full border border-slate-200 px-2 py-1 hover:bg-slate-50">
          <div className="h-8 w-8 rounded-full bg-gradient-to-br from-brand-500 to-brand-700 text-white flex items-center justify-center text-xs font-semibold">
            SD
          </div>
          <span className="hidden sm:inline text-sm text-slate-700">Analyst</span>
          <ChevronDownIcon className="h-4 w-4 text-slate-400" />
        </button>
      </div>
    </header>
  );
}

export default Header;
