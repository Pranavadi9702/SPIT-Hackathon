import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { auth } from "../firebase";
import { onAuthStateChanged } from "firebase/auth";
import Avatar from "../components/Avatar";

function Settings() {
  const navigate = useNavigate();

  // User details (uses Firebase auth when available)
  const [user, setUser] = useState({
    name: "Analyst User",
    email: "analyst@chainforecast.ai",
    role: "Sales & CRM Analyst",
    photoURL: null,
  });

  useEffect(() => {
    const unsub = onAuthStateChanged(auth, (u) => {
      if (u) {
        setUser((prev) => ({
          ...prev,
          name: u.displayName || prev.name,
          email: u.email || prev.email,
          photoURL: u.photoURL || null,
        }));
      }
    });
    return () => unsub();
  }, []);

  // Password update state
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [passwordErrors, setPasswordErrors] = useState({});
  const [passwordSuccess, setPasswordSuccess] = useState("");

  // Delete account state
  const [deleteText, setDeleteText] = useState("");
  const [deleteMessage, setDeleteMessage] = useState("");

  const handlePasswordUpdate = (e) => {
    e.preventDefault();
    const errors = {};

    if (!currentPassword.trim()) errors.current = "Current password is required.";
    if (!newPassword.trim()) errors.new = "New password is required.";
    if (!confirmPassword.trim()) {
      errors.confirm = "Please confirm your new password.";
    } else if (newPassword !== confirmPassword) {
      errors.confirm = "Passwords do not match.";
    }

    setPasswordErrors(errors);
    setPasswordSuccess("");

    if (Object.keys(errors).length === 0) {
      // TODO: call real API later
      setPasswordSuccess("Password updated successfully.");
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
    }
  };

  const handleDeleteAccount = (e) => {
    e.preventDefault();
    setDeleteMessage("");

    if (deleteText !== "DELETE") {
      setDeleteMessage('Please type "DELETE" to confirm.');
      return;
    }

    // TODO: call real delete API later
    setDeleteMessage("Account deleted. Redirecting to login…");

    setTimeout(() => {
      // clear any auth if you add it later
      // localStorage.removeItem("authToken");
      navigate("/login");
    }, 1500);
  };

  return (
    <div className="space-y-6">
      {/* Profile card */}
      <div className="bg-white/90 dark:bg-slate-900/80 rounded-2xl shadow-sm border border-slate-100 dark:border-slate-700 p-4 lg:p-6 text-sm flex flex-col gap-4">
        <div className="flex items-start justify-between gap-4">
          <div className="flex items-center gap-4">
            <Avatar
              src={user?.photoURL}
              name={user?.name || "Analyst User"}
              size="h-12 w-12 text-lg"
            />
            <div>
              <h2 className="text-sm font-semibold text-slate-900 dark:text-slate-100">
                Profile
              </h2>
              <p className="text-xs text-slate-500 dark:text-slate-400">
                Manage your ChainForecast account details.
              </p>
            </div>
          </div>
        </div>

        <div className="grid gap-4 md:grid-cols-3">
          <div className="text-xs">
            <p className="text-slate-500 dark:text-slate-400 mb-0.5">
              Full name
            </p>
            <p className="font-medium text-slate-900 dark:text-slate-100">
              {user.name}
            </p>
          </div>
          <div className="text-xs">
            <p className="text-slate-500 dark:text-slate-400 mb-0.5">
              Work email
            </p>
            <p className="font-medium text-slate-900 dark:text-slate-100">
              {user.email}
            </p>
          </div>
          <div className="text-xs">
            <p className="text-slate-500 dark:text-slate-400 mb-0.5">Role</p>
            <p className="font-medium text-slate-900 dark:text-slate-100">
              {user.role}
            </p>
          </div>
        </div>

      </div>

      {/* Password + danger zone */}
      <div className="grid gap-6 lg:grid-cols-3">
        {/* Password update */}
        <div className="bg-white/90 dark:bg-slate-900/80 rounded-2xl shadow-sm border border-slate-100 dark:border-slate-700 p-4 lg:p-6 text-sm lg:col-span-2">
          <h3 className="text-sm font-semibold text-slate-900 dark:text-slate-100 mb-1">
            Update password
          </h3>
          <p className="text-xs text-slate-500 dark:text-slate-400 mb-4">
            Keep your account secure by using a strong, unique password.
          </p>

          <form onSubmit={handlePasswordUpdate} className="space-y-4 text-xs">
            <div>
              <label className="block font-medium text-slate-700 dark:text-slate-200 mb-1">
                Current password
              </label>
              <input
                type="password"
                className={`w-full rounded-xl border px-3 py-2 bg-slate-50 dark:bg-slate-900/80 text-slate-900 dark:text-slate-100 placeholder:text-slate-400 dark:placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/40 ${
                  passwordErrors.current
                    ? "border-rose-300"
                    : "border-slate-200 dark:border-slate-700"
                }`}
                placeholder="Enter current password"
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
              />
              {passwordErrors.current && (
                <p className="mt-1 text-[11px] text-rose-500">
                  {passwordErrors.current}
                </p>
              )}
            </div>

            <div className="grid gap-4 md:grid-cols-2">
              <div>
                <label className="block font-medium text-slate-700 dark:text-slate-200 mb-1">
                  New password
                </label>
                <input
                  type="password"
                  className={`w-full rounded-xl border px-3 py-2 bg-slate-50 dark:bg-slate-900/80 text-slate-900 dark:text-slate-100 placeholder:text-slate-400 dark:placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/40 ${
                    passwordErrors.new
                      ? "border-rose-300"
                      : "border-slate-200 dark:border-slate-700"
                  }`}
                  placeholder="Create a new password"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                />
                {passwordErrors.new && (
                  <p className="mt-1 text-[11px] text-rose-500">
                    {passwordErrors.new}
                  </p>
                )}
              </div>

              <div>
                <label className="block font-medium text-slate-700 dark:text-slate-200 mb-1">
                  Confirm new password
                </label>
                <input
                  type="password"
                  className={`w-full rounded-xl border px-3 py-2 bg-slate-50 dark:bg-slate-900/80 text-slate-900 dark:text-slate-100 placeholder:text-slate-400 dark:placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/40 ${
                    passwordErrors.confirm
                      ? "border-rose-300"
                      : "border-slate-200 dark:border-slate-700"
                  }`}
                  placeholder="Repeat new password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                />
                {passwordErrors.confirm && (
                  <p className="mt-1 text-[11px] text-rose-500">
                    {passwordErrors.confirm}
                  </p>
                )}
              </div>
            </div>

            <div className="flex items-center justify-between mt-2">
              <p className="text-[11px] text-slate-500 dark:text-slate-400">
                Password should be at least 8 characters with numbers & symbols.
              </p>
              <button
                type="submit"
                className="inline-flex items-center justify-center rounded-full bg-slate-900 text-white px-4 py-2 text-xs font-medium shadow-sm hover:bg-black transition"
              >
                Save changes
              </button>
            </div>

            {passwordSuccess && (
              <p className="mt-2 text-[11px] text-emerald-600 dark:text-emerald-400">
                {passwordSuccess}
              </p>
            )}
          </form>
        </div>

        {/* Danger zone */}
        <div className="bg-white/90 dark:bg-slate-900/80 rounded-2xl shadow-sm border border-rose-100 dark:border-rose-700/60 p-4 lg:p-6 text-xs">
          <h3 className="text-sm font-semibold text-rose-600 dark:text-rose-400 mb-1">
            Danger zone
          </h3>
          <p className="text-[11px] text-slate-600 dark:text-slate-400 mb-3">
            Deleting your account will remove your access to the ChainForecast
            dashboard. This action cannot be undone.
          </p>

          <form onSubmit={handleDeleteAccount} className="space-y-3">
            <div>
              <label className="block font-medium text-slate-700 dark:text-slate-200 mb-1">
                Confirm deletion
              </label>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 mb-1">
                Type{" "}
                <span className="font-semibold text-slate-900 dark:text-slate-100">
                  DELETE
                </span>{" "}
                in all caps to confirm account deletion.
              </p>
              <input
                type="text"
                className="w-full rounded-xl border px-3 py-2 bg-slate-50 dark:bg-slate-900/80 text-slate-900 dark:text-slate-100 placeholder:text-slate-400 dark:placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-rose-500/40 border-slate-200 dark:border-slate-700"
                placeholder='Type "DELETE" to confirm'
                value={deleteText}
                onChange={(e) => setDeleteText(e.target.value)}
              />
            </div>

            <button
              type="submit"
              className="w-full rounded-full bg-rose-600 text-white py-2 text-xs font-medium shadow-sm hover:bg-rose-700 transition disabled:opacity-60 disabled:cursor-not-allowed"
              disabled={deleteText !== "DELETE"}
            >
              Delete my account
            </button>

            {deleteMessage && (
              <p className="mt-1 text-[11px] text-center text-rose-600 dark:text-rose-400">
                {deleteMessage}
              </p>
            )}
          </form>
        </div>
      </div>
    </div>
  );
}

export default Settings;