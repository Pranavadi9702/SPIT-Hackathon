import React, { useState, useEffect } from "react";
import { onAuthStateChanged } from "firebase/auth";
import { auth } from "../firebase";

export default function Avatar({ src, name, size = "h-8 w-8", className = "", alt }) {
  const initials = (name || "")
    .split(" ")
    .map((n) => n[0])
    .filter(Boolean)
    .slice(0, 2)
    .join("")
    .toUpperCase();

  if (src) {
    return (
      <img
        src={src}
        alt={alt || name || "avatar"}
        className={`${size} rounded-full object-cover ${className}`}
      />
    );
  }

  return (
    <div
      className={`${size} rounded-full bg-indigo-600 text-white flex items-center justify-center font-semibold ${className}`}
    >
      {initials || "CF"}
    </div>
  );
}

function Header() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const unsub = onAuthStateChanged(auth, (u) => setUser(u || null));
    return () => unsub();
  }, []);

  return (
    <div className="relative">
      <button className="flex items-center gap-2 rounded-full px-2 py-1 border border-white/10">
        <Avatar
          src={user?.photoURL}
          name={user?.displayName || "Analyst"}
          size="h-8 w-8"
          className="border border-white/10"
        />
        <span className="text-sm">Analyst</span>
      </button>
    </div>
  );
}