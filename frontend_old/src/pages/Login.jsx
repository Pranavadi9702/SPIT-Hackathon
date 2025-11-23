import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { auth, googleProvider } from "../firebase"; // 👈 adjust path if needed
import {
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signInWithPopup,
  updateProfile,
} from "firebase/auth";
import { onAuthStateChanged } from "firebase/auth";
import Avatar from "../components/Avatar";

function Login() {
  const navigate = useNavigate();

  const [signedInUser, setSignedInUser] = useState(null);
  useEffect(() => {
    const unsub = onAuthStateChanged(auth, (u) => {
      setSignedInUser(u || null);
    });
    return () => unsub();
  }, []);

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
    <div className="min-h-screen flex items-center justify-center bg-slate-100 px-4 py-6">
      <div className="w-full max-w-5xl">
        {/* Outer frame */}
        <div className="relative grid grid-cols-1 md:grid-cols-2 gap-0 rounded-[32px] bg-transparent">
          {/* Left hero panel */}
          <div className="relative overflow-hidden rounded-t-[32px] md:rounded-l-[32px] md:rounded-tr-none bg-slate-950 text-white px-8 py-8 flex flex-col">
            {/* Decorative shapes */}
            <div className="pointer-events-none absolute -top-24 -left-20 h-72 w-72 rounded-full border-[14px] border-slate-400/30" />
            <div className="pointer-events-none absolute 10 -bottom-24 -right-10 h-80 w-80 rounded-full border-[14px] border-slate-500/25" />
            <div className="pointer-events-none absolute inset-0 bg-gradient-to-br from-slate-900/40 via-slate-900/10 to-black/90" />

            {/* Content above overlay */}
            <div className="relative flex-1 flex flex-col">
              {/* Top brand + nav */}
              <div className="flex items-center justify-between mb-10">
                <div className="flex items-center gap-3">
                  {signedInUser ? (
                    <Avatar
                      src={signedInUser.photoURL}
                      name={signedInUser.displayName || "User"}
                      size="h-9 w-9 text-sm"
                      className="border border-white/20"
                    />
                  ) : (
                    <div className="h-9 w-9 rounded-2xl bg-white/10 border border-white/20 flex items-center justify-center text-sm font-semibold shadow-lg">
                      CF
                    </div>
                  )}
                  <span className="text-sm font-semibold tracking-wide">
                    ChainForecast
                  </span>
                </div>
              </div>

              {/* Center message */}
              <div className="mt-auto mb-8">
                <p className="text-[11px] tracking-[0.2em] uppercase text-slate-400 mb-3">
                  AI SALES FORECAST &amp; CRM
                </p>
                <h1 className="text-3xl md:text-4xl font-semibold leading-tight">
                  Welcome back,
                  <br />
                  Analyst.
                </h1>
                <p className="mt-3 text-sm text-slate-300 max-w-xs">
                  Log in to explore revenue forecasts, customer segments and
                  campaign insights in a single dashboard.
                </p>
              </div>
            </div>

            {/* Bottom info */}
            <div className="relative flex items-center justify-between text-[11px] text-slate-400">
              <span>Secure access • SSO ready • Role-based controls</span>
            </div>
          </div>

          {/* Right auth panel */}
          <div className="bg-white rounded-b-[32px] md:rounded-r-[32px] md:rounded-bl-none shadow-[0_30px_60px_rgba(15,23,42,0.18)] border border-slate-200 px-7 sm:px-9 py-7 sm:py-9 flex flex-col">
            {/* Small brand for mobile (right auth panel) */}
            <div className="md:hidden mb-4 flex items-center gap-2">
              {signedInUser ? (
                <Avatar src={signedInUser.photoURL} name={signedInUser.displayName || "User"} size="h-7 w-7 text-xs" />
              ) : (
                <div className="h-7 w-7 rounded-xl bg-slate-900 text-white flex items-center justify-center text-xs font-semibold">
                  CF
                </div>
              )}
              <span className="text-xs font-semibold text-slate-700">
                ChainForecast
              </span>
            </div>

            {/* Log in / Sign up toggle */}
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold text-slate-900">
                {activeTab === "login" ? "Log in" : "Sign up"}
              </h2>

              <div className="inline-flex rounded-full bg-slate-100 px-1 py-1 text-[11px] font-medium">
                <button
                  type="button"
                  onClick={() => {
                    setActiveTab("login");
                    setGlobalError("");
                    setGlobalMessage("");
                  }}
                  className={`px-3 py-1 rounded-full transition ${
                    activeTab === "login"
                      ? "bg-slate-900 text-white shadow-sm"
                      : "text-slate-500 hover:text-slate-800"
                  }`}
                >
                  Log in
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setActiveTab("signup");
                    setGlobalError("");
                    setGlobalMessage("");
                  }}
                  className={`px-3 py-1 rounded-full transition ${
                    activeTab === "signup"
                      ? "bg-slate-900 text-white shadow-sm"
                      : "text-slate-500 hover:text-slate-800"
                  }`}
                >
                  Sign up
                </button>
              </div>
            </div>

            <p className="text-xs text-slate-500 mb-5">
              {activeTab === "login"
                ? "Enter your details to access the ChainForecast dashboard."
                : "Create your analyst account to start forecasting sales and segmenting customers."}
            </p>

            {/* Global alert (from logic) */}
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

            {/* LOGIN FORM */}
            {activeTab === "login" && (
              <form onSubmit={handleLoginSubmit} className="space-y-4 text-sm">
                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1.5">
                    Work Email
                  </label>
                  <div
                    className={`flex items-center rounded-full px-3 py-2 border text-xs bg-slate-100 ${
                      loginErrors.email ? "border-red-300" : "border-slate-200"
                    }`}
                  >
                    <span className="mr-2 text-slate-400 text-[13px]">@</span>
                    <input
                      type="email"
                      className="w-full bg-transparent outline-none text-slate-900 placeholder:text-slate-400"
                      placeholder="you@company.com"
                      value={loginEmail}
                      onChange={(e) => setLoginEmail(e.target.value)}
                    />
                  </div>
                  {loginErrors.email && (
                    <p className="text-xs text-red-500 mt-1">
                      {loginErrors.email}
                    </p>
                  )}
                </div>

                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1.5">
                    Password
                  </label>
                  <div
                    className={`flex items-center rounded-full px-3 py-2 border text-xs bg-slate-100 ${
                      loginErrors.password ? "border-red-300" : "border-slate-200"
                    }`}
                  >
                    <span className="mr-2 text-slate-400 text-[13px]">•••</span>
                    <input
                      type="password"
                      className="w-full bg-transparent outline-none text-slate-900 placeholder:text-slate-400"
                      placeholder="Enter your password"
                      value={loginPassword}
                      onChange={(e) => setLoginPassword(e.target.value)}
                    />
                  </div>
                  {loginErrors.password && (
                    <p className="text-xs text-red-500 mt-1">
                      {loginErrors.password}
                    </p>
                  )}
                </div>

                <div className="flex items-center justify-between text-[11px]">
                  <label className="inline-flex items-center gap-2 text-slate-600">
                    <input
                      type="checkbox"
                      className="rounded border-slate-300"
                      checked={rememberMe}
                      onChange={(e) => setRememberMe(e.target.checked)}
                    />
                    <span>Remember me</span>
                  </label>
                  <button
                    type="button"
                    className="text-slate-400 hover:text-slate-700"
                  >
                    Forgot password?
                  </button>
                </div>

                <button
                  type="submit"
                  disabled={loginLoading}
                  className="w-full mt-2 rounded-full bg-slate-900 text-white font-medium py-2.5 text-sm shadow-sm hover:bg-black transition disabled:opacity-60 disabled:cursor-not-allowed"
                >
                  {loginLoading ? "Logging in..." : "Log in"}
                </button>

                <div className="flex items-center gap-3 my-3">
                  <div className="h-px flex-1 bg-slate-200" />
                  <span className="text-[11px] text-slate-400">or</span>
                  <div className="h-px flex-1 bg-slate-200" />
                </div>

                <button
                  type="button"
                  onClick={handleGoogleLogin}
                  className="w-full rounded-full bg-slate-100 text-slate-700 font-medium py-2.5 text-sm hover:bg-slate-200 transition"
                >
                  Continue with Google
                </button>

                <button
                  type="button"
                  onClick={() => setActiveTab("signup")}
                  className="w-full mt-3 rounded-full bg-slate-100 text-slate-700 font-medium py-2.5 text-sm hover:bg-slate-200 transition"
                >
                  Create a new account
                </button>
              </form>
            )}

            {/* SIGNUP FORM */}
            {activeTab === "signup" && (
              <form onSubmit={handleSignupSubmit} className="space-y-4 text-sm">
                <div className="grid grid-cols-1 gap-3">
                  <div>
                    <label className="block text-xs font-medium text-slate-700 mb-1.5">
                      Full name
                    </label>
                    <div
                      className={`flex items-center rounded-full px-3 py-2 border text-xs bg-slate-100 ${
                        signupErrors.name ? "border-red-300" : "border-slate-200"
                      }`}
                    >
                      <input
                        type="text"
                        className="w-full bg-transparent outline-none text-slate-900 placeholder:text-slate-400"
                        placeholder="Your name"
                        value={signupName}
                        onChange={(e) => setSignupName(e.target.value)}
                      />
                    </div>
                    {signupErrors.name && (
                      <p className="text-xs text-red-500 mt-1">
                        {signupErrors.name}
                      </p>
                    )}
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-slate-700 mb-1.5">
                      Work email
                    </label>
                    <div
                      className={`flex items-center rounded-full px-3 py-2 border text-xs bg-slate-100 ${
                        signupErrors.email ? "border-red-300" : "border-slate-200"
                      }`}
                    >
                      <span className="mr-2 text-slate-400 text-[13px]">@</span>
                      <input
                        type="email"
                        className="w-full bg-transparent outline-none text-slate-900 placeholder:text-slate-400"
                        placeholder="you@company.com"
                        value={signupEmail}
                        onChange={(e) => setSignupEmail(e.target.value)}
                      />
                    </div>
                    {signupErrors.email && (
                      <p className="text-xs text-red-500 mt-1">
                        {signupErrors.email}
                      </p>
                    )}
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1.5">
                    Password
                  </label>
                  <div
                    className={`flex items-center rounded-full px-3 py-2 border text-xs bg-slate-100 ${
                      signupErrors.password ? "border-red-300" : "border-slate-200"
                    }`}
                  >
                    <span className="mr-2 text-slate-400 text-[13px]">•••</span>
                    <input
                      type="password"
                      className="w-full bg-transparent outline-none text-slate-900 placeholder:text-slate-400"
                      placeholder="Create a password"
                      value={signupPassword}
                      onChange={(e) => setSignupPassword(e.target.value)}
                    />
                  </div>
                  {signupErrors.password && (
                    <p className="text-xs text-red-500 mt-1">
                      {signupErrors.password}
                    </p>
                  )}
                </div>

                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1.5">
                    Confirm password
                  </label>
                  <div
                    className={`flex items-center rounded-full px-3 py-2 border text-xs bg-slate-100 ${
                      signupErrors.confirmPassword
                        ? "border-red-300"
                        : "border-slate-200"
                    }`}
                  >
                    <input
                      type="password"
                      className="w-full bg-transparent outline-none text-slate-900 placeholder:text-slate-400"
                      placeholder="Repeat your password"
                      value={signupConfirmPassword}
                      onChange={(e) => setSignupConfirmPassword(e.target.value)}
                    />
                  </div>
                  {signupErrors.confirmPassword && (
                    <p className="text-xs text-red-500 mt-1">
                      {signupErrors.confirmPassword}
                    </p>
                  )}
                </div>

                <button
                  type="submit"
                  disabled={signupLoading}
                  className="w-full mt-1 rounded-full bg-slate-900 text-white font-medium py-2.5 text-sm shadow-sm hover:bg-black transition disabled:opacity-60 disabled:cursor-not-allowed"
                >
                  {signupLoading ? "Creating account..." : "Create account"}
                </button>

                <p className="text-[11px] text-slate-400 text-center mt-2">
                  Already have an account?{" "}
                  <button
                    type="button"
                    onClick={() => setActiveTab("login")}
                    className="underline underline-offset-2 text-slate-700"
                  >
                    Log in
                  </button>
                </p>
              </form>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;