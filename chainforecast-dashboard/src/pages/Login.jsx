import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Login() {
  const navigate = useNavigate();

  const [activeTab, setActiveTab] = useState("login"); // "login" | "signup"

  // Login form state
  const [loginEmail, setLoginEmail] = useState("");
  const [loginPassword, setLoginPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(true);
  const [loginErrors, setLoginErrors] = useState({});

  // Signup form state
  const [signupName, setSignupName] = useState("");
  const [signupEmail, setSignupEmail] = useState("");
  const [signupPassword, setSignupPassword] = useState("");
  const [signupConfirmPassword, setSignupConfirmPassword] = useState("");
  const [signupErrors, setSignupErrors] = useState({});

  const handleLoginSubmit = (e) => {
    e.preventDefault();
    const errors = {};
    if (!loginEmail.trim()) errors.email = "Email is required.";
    if (!loginPassword.trim()) errors.password = "Password is required.";
    setLoginErrors(errors);

    if (Object.keys(errors).length === 0) {
      // TODO: replace with real auth call later
      // For now just navigate to dashboard
      navigate("/overview");
    }
  };

  const handleSignupSubmit = (e) => {
    e.preventDefault();
    const errors = {};
    if (!signupName.trim()) errors.name = "Full name is required.";
    if (!signupEmail.trim()) errors.email = "Email is required.";
    if (!signupPassword.trim()) errors.password = "Password is required.";
    if (!signupConfirmPassword.trim()) {
      errors.confirmPassword = "Please confirm your password.";
    } else if (signupPassword !== signupConfirmPassword) {
      errors.confirmPassword = "Passwords do not match.";
    }

    setSignupErrors(errors);

    if (Object.keys(errors).length === 0) {
      // TODO: send signup data to backend later
      // For now just show a fake success + switch to login
      alert("Signup successful (frontend only). You can now log in.");
      setActiveTab("login");
      setLoginEmail(signupEmail);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950 px-4">
      <div className="w-full max-w-md bg-white rounded-3xl shadow-2xl p-6 sm:p-8 border border-slate-100">
        {/* Logo + title */}
        <div className="flex items-center gap-3 mb-6">
          <div className="h-10 w-10 rounded-2xl bg-gradient-to-br from-brand-500 to-brand-700 text-white flex items-center justify-center font-semibold">
            CF
          </div>
          <div>
            <div className="text-sm font-semibold text-slate-900">
              ChainForecast
            </div>
            <div className="text-xs text-slate-500">
              AI-Powered Sales Forecasting & CRM
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex mb-6 bg-slate-100 rounded-2xl p-1 text-xs font-medium">
          <button
            type="button"
            onClick={() => setActiveTab("login")}
            className={`flex-1 py-2 rounded-2xl transition ${
              activeTab === "login"
                ? "bg-white shadow-sm text-slate-900"
                : "text-slate-500 hover:text-slate-800"
            }`}
          >
            Login
          </button>
          <button
            type="button"
            onClick={() => setActiveTab("signup")}
            className={`flex-1 py-2 rounded-2xl transition ${
              activeTab === "signup"
                ? "bg-white shadow-sm text-slate-900"
                : "text-slate-500 hover:text-slate-800"
            }`}
          >
            Sign Up
          </button>
        </div>

        {/* Heading + subtitle */}
        {activeTab === "login" ? (
          <>
            <h1 className="text-lg font-semibold text-slate-900 mb-1">
              Welcome back
            </h1>
            <p className="text-xs text-slate-500 mb-4">
              Login to access ChainForecast analytics dashboard.
            </p>
          </>
        ) : (
          <>
            <h1 className="text-lg font-semibold text-slate-900 mb-1">
              Create analyst account
            </h1>
            <p className="text-xs text-slate-500 mb-4">
              Sign up to get access.
            </p>
          </>
        )}

        {/* LOGIN FORM */}
        {activeTab === "login" && (
          <form onSubmit={handleLoginSubmit} className="space-y-4 text-sm">
            <div>
              <label className="block text-xs font-medium text-slate-700 mb-1">
                Work Email
              </label>
              <input
                type="email"
                className={`w-full border rounded-xl px-3 py-2 focus:outline-none focus:ring-2 text-sm ${
                  loginErrors.email
                    ? "border-red-300 focus:ring-red-200"
                    : "border-slate-200 focus:ring-brand-100"
                }`}
                placeholder="you@company.com"
                value={loginEmail}
                onChange={(e) => setLoginEmail(e.target.value)}
              />
              {loginErrors.email && (
                <p className="text-xs text-red-500 mt-1">{loginErrors.email}</p>
              )}
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-700 mb-1">
                Password
              </label>
              <input
                type="password"
                className={`w-full border rounded-xl px-3 py-2 focus:outline-none focus:ring-2 text-sm ${
                  loginErrors.password
                    ? "border-red-300 focus:ring-red-200"
                    : "border-slate-200 focus:ring-brand-100"
                }`}
                placeholder="••••••••"
                value={loginPassword}
                onChange={(e) => setLoginPassword(e.target.value)}
              />
              {loginErrors.password && (
                <p className="text-xs text-red-500 mt-1">
                  {loginErrors.password}
                </p>
              )}
            </div>

            <div className="flex items-center justify-between text-xs">
              <label className="inline-flex items-center gap-2">
                <input
                  type="checkbox"
                  className="rounded border-slate-300"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                />
                <span className="text-slate-600">Remember me</span>
              </label>
              <span className="text-slate-400">For authorized analysts only</span>
            </div>

            <button
              type="submit"
              className="w-full mt-2 bg-gradient-to-r from-brand-500 to-brand-700 text-white font-medium py-2.5 rounded-xl text-sm shadow-sm hover:shadow-md transition"
            >
              Login
            </button>
          </form>
        )}

        {/* SIGNUP FORM */}
        {activeTab === "signup" && (
          <form onSubmit={handleSignupSubmit} className="space-y-4 text-sm">
            <div>
              <label className="block text-xs font-medium text-slate-700 mb-1">
                Full Name
              </label>
              <input
                type="text"
                className={`w-full border rounded-xl px-3 py-2 focus:outline-none focus:ring-2 text-sm ${
                  signupErrors.name
                    ? "border-red-300 focus:ring-red-200"
                    : "border-slate-200 focus:ring-brand-100"
                }`}
                placeholder="Your name"
                value={signupName}
                onChange={(e) => setSignupName(e.target.value)}
              />
              {signupErrors.name && (
                <p className="text-xs text-red-500 mt-1">{signupErrors.name}</p>
              )}
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-700 mb-1">
                Work Email
              </label>
              <input
                type="email"
                className={`w-full border rounded-xl px-3 py-2 focus:outline-none focus:ring-2 text-sm ${
                  signupErrors.email
                    ? "border-red-300 focus:ring-red-200"
                    : "border-slate-200 focus:ring-brand-100"
                }`}
                placeholder="you@company.com"
                value={signupEmail}
                onChange={(e) => setSignupEmail(e.target.value)}
              />
              {signupErrors.email && (
                <p className="text-xs text-red-500 mt-1">{signupErrors.email}</p>
              )}
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-700 mb-1">
                Password
              </label>
              <input
                type="password"
                className={`w-full border rounded-xl px-3 py-2 focus:outline-none focus:ring-2 text-sm ${
                  signupErrors.password
                    ? "border-red-300 focus:ring-red-200"
                    : "border-slate-200 focus:ring-brand-100"
                }`}
                placeholder="Create a password"
                value={signupPassword}
                onChange={(e) => setSignupPassword(e.target.value)}
              />
              {signupErrors.password && (
                <p className="text-xs text-red-500 mt-1">
                  {signupErrors.password}
                </p>
              )}
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-700 mb-1">
                Confirm Password
              </label>
              <input
                type="password"
                className={`w-full border rounded-xl px-3 py-2 focus:outline-none focus:ring-2 text-sm ${
                  signupErrors.confirmPassword
                    ? "border-red-300 focus:ring-red-200"
                    : "border-slate-200 focus:ring-brand-100"
                }`}
                placeholder="Repeat your password"
                value={signupConfirmPassword}
                onChange={(e) => setSignupConfirmPassword(e.target.value)}
              />
              {signupErrors.confirmPassword && (
                <p className="text-xs text-red-500 mt-1">
                  {signupErrors.confirmPassword}
                </p>
              )}
            </div>

            <button
              type="submit"
              className="w-full mt-1 bg-slate-900 text-white font-medium py-2.5 rounded-xl text-sm shadow-sm hover:bg-slate-800 transition"
            >
              Create Account
            </button>
          </form>
        )}
      </div>
    </div>
  );
}

export default Login;
