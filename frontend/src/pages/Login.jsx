import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { auth, googleProvider } from "../firebase"; // 👈 adjust path if needed
import {
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signInWithPopup,
  updateProfile,
} from "firebase/auth";

function Login() {
  const navigate = useNavigate();

  const [activeTab, setActiveTab] = useState("login"); // "login" | "signup"

  // Login form state
  const [loginEmail, setLoginEmail] = useState("");
  const [loginPassword, setLoginPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(true);
  const [loginErrors, setLoginErrors] = useState({});
  const [loginLoading, setLoginLoading] = useState(false);

  // Signup form state
  const [signupName, setSignupName] = useState("");
  const [signupEmail, setSignupEmail] = useState("");
  const [signupPassword, setSignupPassword] = useState("");
  const [signupConfirmPassword, setSignupConfirmPassword] = useState("");
  const [signupErrors, setSignupErrors] = useState({});
  const [signupLoading, setSignupLoading] = useState(false);

  // Shared error / info banner
  const [globalError, setGlobalError] = useState("");
  const [globalMessage, setGlobalMessage] = useState("");

  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    setGlobalError("");
    setGlobalMessage("");

    const errors = {};
    if (!loginEmail.trim()) errors.email = "Email is required.";
    if (!loginPassword.trim()) errors.password = "Password is required.";
    setLoginErrors(errors);

    if (Object.keys(errors).length > 0) return;

    try {
      setLoginLoading(true);

      // Optional: control persistence based on rememberMe
      // import { setPersistence, browserLocalPersistence, browserSessionPersistence } from "firebase/auth";
      // await setPersistence(auth, rememberMe ? browserLocalPersistence : browserSessionPersistence);

      await signInWithEmailAndPassword(auth, loginEmail, loginPassword);

      navigate("/overview");
    } catch (err) {
      console.error("Login error:", err);
      setGlobalError(
        err.code === "auth/invalid-credential"
          ? "Invalid email or password."
          : err.message || "Failed to log in. Please try again."
      );
    } finally {
      setLoginLoading(false);
    }
  };

  const handleSignupSubmit = async (e) => {
    e.preventDefault();
    setGlobalError("");
    setGlobalMessage("");

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

    if (Object.keys(errors).length > 0) return;

    try {
      setSignupLoading(true);

      const userCred = await createUserWithEmailAndPassword(
        auth,
        signupEmail,
        signupPassword
      );

      // Set display name
      if (signupName.trim()) {
        await updateProfile(userCred.user, {
          displayName: signupName,
        });
      }

      setGlobalMessage("Signup successful. You can now log in.");
      setActiveTab("login");
      setLoginEmail(signupEmail);
    } catch (err) {
      console.error("Signup error:", err);
      setGlobalError(
        err.code === "auth/email-already-in-use"
          ? "An account with this email already exists."
          : err.message || "Failed to create account. Please try again."
      );
    } finally {
      setSignupLoading(false);
    }
  };

  const handleGoogleLogin = async () => {
    setGlobalError("");
    setGlobalMessage("");

    try {
      // You can add scopes if needed:
      // googleProvider.addScope("https://www.googleapis.com/auth/contacts.readonly");

      await signInWithPopup(auth, googleProvider);
      navigate("/overview");
    } catch (err) {
      console.error("Google login error:", err);
      setGlobalError(
        err.code === "auth/popup-closed-by-user"
          ? "Google sign-in was cancelled."
          : "Failed to sign in with Google. Please try again."
      );
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
        <div className="flex mb-4 bg-slate-100 rounded-2xl p-1 text-xs font-medium">
          <button
            type="button"
            onClick={() => {
              setActiveTab("login");
              setGlobalError("");
              setGlobalMessage("");
            }}
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
            onClick={() => {
              setActiveTab("signup");
              setGlobalError("");
              setGlobalMessage("");
            }}
            className={`flex-1 py-2 rounded-2xl transition ${
              activeTab === "signup"
                ? "bg-white shadow-sm text-slate-900"
                : "text-slate-500 hover:text-slate-800"
            }`}
          >
            Sign Up
          </button>
        </div>

        {/* Global alert */}
        {(globalError || globalMessage) && (
          <div
            className={`mb-4 text-xs px-3 py-2 rounded-xl border ${
              globalError
                ? "border-red-200 bg-red-50 text-red-600"
                : "border-emerald-200 bg-emerald-50 text-emerald-600"
            }`}
          >
            {globalError || globalMessage}
          </div>
        )}

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
          <>
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
                  <p className="text-xs text-red-500 mt-1">
                    {loginErrors.email}
                  </p>
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
                <span className="text-slate-400">
                  For authorized analysts only
                </span>
              </div>

              <button
                type="submit"
                disabled={loginLoading}
                className="w-full mt-2 bg-gradient-to-r from-brand-500 to-brand-700 text-white font-medium py-2.5 rounded-xl text-sm shadow-sm hover:shadow-md disabled:opacity-60 disabled:cursor-not-allowed transition"
              >
                {loginLoading ? "Logging in..." : "Login"}
              </button>
            </form>

            {/* Divider + Google button */}
            <div className="flex items-center my-4">
              <div className="flex-1 h-px bg-slate-200" />
              <span className="px-2 text-[10px] uppercase tracking-wide text-slate-400">
                or
              </span>
              <div className="flex-1 h-px bg-slate-200" />
            </div>

            <button
              type="button"
              onClick={handleGoogleLogin}
              className="w-full border border-slate-200 rounded-xl py-2.5 text-xs font-medium flex items-center justify-center gap-2 hover:bg-slate-50 transition"
            >
              {/* You can replace this with a Google icon SVG */}
              <span className="h-4 w-4 rounded-full bg-white border border-slate-200 flex items-center justify-center text-[10px]">
                G
              </span>
              <span>Continue with Google</span>
            </button>
          </>
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
                <p className="text-xs text-red-500 mt-1">
                  {signupErrors.name}
                </p>
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
                <p className="text-xs text-red-500 mt-1">
                  {signupErrors.email}
                </p>
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
              disabled={signupLoading}
              className="w-full mt-1 bg-slate-900 text-white font-medium py-2.5 rounded-xl text-sm shadow-sm hover:bg-slate-800 disabled:opacity-60 disabled:cursor-not-allowed transition"
            >
              {signupLoading ? "Creating account..." : "Create Account"}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}

export default Login;
