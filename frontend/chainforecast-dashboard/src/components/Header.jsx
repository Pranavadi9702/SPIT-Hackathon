import { useState, useEffect, useRef } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import {
  BellIcon,
  ChevronDownIcon,
  MagnifyingGlassIcon,
  MoonIcon,
  SunIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
} from "@heroicons/react/24/outline";

const titleMap = {
  "/overview": "Overview",
  "/sales-forecast": "Sales Forecast",
  "/customer-segmentation": "Customer Segmentation",
  "/offers": "Offers",
  "/settings": "Settings",
};

function Header({ theme = "light", toggleTheme }) {
  const location = useLocation();
  const navigate = useNavigate();

  const title = titleMap[location.pathname] || "Dashboard";
  const isDark = theme === "dark";

  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [showLogoutConfirm, setShowLogoutConfirm] = useState(false);
  const [showLogoutSuccess, setShowLogoutSuccess] = useState(false);

  const profileButtonRef = useRef(null);
  const menuRef = useRef(null);

  // Close dropdown on click outside
  useEffect(() => {
    function handleClickOutside(e) {
      if (
        menuRef.current &&
        !menuRef.current.contains(e.target) &&
        profileButtonRef.current &&
        !profileButtonRef.current.contains(e.target)
      ) {
        setIsMenuOpen(false);
      }
    }

    if (isMenuOpen) {
      document.addEventListener("mousedown", handleClickOutside);
    }

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [isMenuOpen]);

  const handleSettings = () => {
    setIsMenuOpen(false);
    navigate("/settings");
  };

  // Open confirmation dialog instead of logout directly
  const handleLogoutClick = () => {
    setIsMenuOpen(false);
    setShowLogoutConfirm(true);
  };

  const confirmLogout = () => {
    setShowLogoutConfirm(false);
    setShowLogoutSuccess(true);
    setTimeout(() => {
      navigate("/login");
    }, 1200);
  };

  return (
    <>
      <header className="h-16 border-b border-slate-200 dark:border-slate-700 bg-white/80 dark:bg-slate-900/80 backdrop-blur flex items-center justify-between px-4 sm:px-6 lg:px-8">
        <h1 className="text-lg sm:text-xl font-semibold tracking-tight text-slate-900 dark:text-slate-100">
          {title}
        </h1>

        <div className="flex items-center gap-3">
          {/* Search */}
          <div className="hidden sm:flex items-center bg-slate-100 dark:bg-slate-800 rounded-full px-3 py-1.5">
            <MagnifyingGlassIcon className="h-4 w-4 text-slate-400" />
            <input
              type="text"
              placeholder="Search in ChainForecast..."
              className="bg-transparent border-none focus:outline-none text-sm px-2 w-40 lg:w-56 placeholder:text-slate-400 dark:placeholder:text-slate-500 text-slate-800 dark:text-slate-100"
            />
          </div>

          {/* Notifications */}
          <button className="relative p-2 rounded-full hover:bg-slate-100 dark:hover:bg-slate-800">
            <BellIcon className="h-5 w-5 text-slate-500 dark:text-slate-300" />
            <span className="absolute top-1 right-1 inline-flex h-2 w-2 rounded-full bg-red-500" />
          </button>

          {/* Theme toggle */}
          <button
            type="button"
            onClick={toggleTheme}
            className="p-2 rounded-full border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 flex items-center justify-center"
          >
            {isDark ? (
              <SunIcon className="h-5 w-5 text-yellow-400" />
            ) : (
              <MoonIcon className="h-5 w-5 text-slate-600" />
            )}
          </button>

          {/* Profile dropdown */}
          <div className="relative">
            <button
              ref={profileButtonRef}
              type="button"
              onClick={() => setIsMenuOpen((prev) => !prev)}
              className="flex items-center gap-2 rounded-full border border-slate-200 dark:border-slate-700 px-2 py-1 hover:bg-slate-50 dark:hover:bg-slate-800"
            >
              <div className="h-8 w-8 rounded-full bg-gradient-to-br from-brand-500 to-brand-700 text-white flex items-center justify-center text-xs font-semibold">
                SD
              </div>
              <span className="hidden sm:inline text-sm text-slate-700 dark:text-slate-100">
                Analyst
              </span>
              <ChevronDownIcon className="h-4 w-4 text-slate-400 dark:text-slate-300" />
            </button>

            {isMenuOpen && (
              <div
                ref={menuRef}
                className="absolute right-0 mt-2 w-40 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 shadow-lg py-1 z-50"
              >
                <button
                  onClick={handleSettings}
                  className="w-full text-left px-4 py-2 text-sm text-slate-700 dark:text-slate-100 hover:bg-slate-100 dark:hover:bg-slate-800"
                >
                  Settings
                </button>
                <button
                  onClick={handleLogoutClick}
                  className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-slate-100 dark:hover:bg-slate-800"
                >
                  Logout
                </button>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Logout confirmation modal */}
      {showLogoutConfirm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 backdrop-blur-sm">
          <div className="relative w-full max-w-sm rounded-3xl bg-white/95 dark:bg-slate-950/95 border border-slate-100/80 dark:border-slate-800 shadow-[0_24px_80px_rgba(15,23,42,0.45)] px-6 py-6">
            {/* Accent circle */}
            <div className="flex justify-center mb-4">
              <div className="h-12 w-12 rounded-full bg-gradient-to-tr from-rose-500 via-amber-400 to-amber-300 flex items-center justify-center shadow-md">
                <ExclamationTriangleIcon className="h-6 w-6 text-white" />
              </div>
            </div>

            <h2 className="text-lg font-semibold text-center text-slate-900 dark:text-slate-50">
              Log out of ChainForecast?
            </h2>
            <p className="mt-2 text-sm text-center text-slate-600 dark:text-slate-400">
              You’ll be signed out of your dashboard. You can log back in any
              time with your analyst credentials.
            </p>

            <div className="mt-5 flex flex-col-reverse sm:flex-row gap-2 sm:gap-3">
              <button
                onClick={() => setShowLogoutConfirm(false)}
                className="flex-1 rounded-full border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 py-2.5 text-sm font-medium text-slate-700 dark:text-slate-100 hover:bg-slate-100 dark:hover:bg-slate-800 transition"
              >
                Stay logged in
              </button>
              <button
                onClick={confirmLogout}
                className="flex-1 rounded-full bg-rose-600 py-2.5 text-sm font-medium text-white shadow-sm hover:bg-rose-700 transition"
              >
                Yes, log me out
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Logout success modal */}
      {showLogoutSuccess && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 backdrop-blur-sm">
          <div className="w-full max-w-xs rounded-3xl bg-white/95 dark:bg-slate-950/95 border border-slate-100/80 dark:border-slate-800 shadow-[0_20px_60px_rgba(15,23,42,0.38)] px-6 py-5 text-center">
            <div className="flex justify-center mb-3">
              <div className="h-10 w-10 rounded-full bg-emerald-500 flex items-center justify-center">
                <CheckCircleIcon className="h-6 w-6 text-white" />
              </div>
            </div>
            <h2 className="text-sm font-semibold text-emerald-600 dark:text-emerald-400">
              Logout successful
            </h2>
            <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
              Redirecting you to the login screen…
            </p>
          </div>
        </div>
      )}
    </>
  );
}

export default Header;