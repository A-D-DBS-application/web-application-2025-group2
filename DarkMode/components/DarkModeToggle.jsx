import React, { useEffect, useState } from "react";
import "./DarkModeToggle.css";

function DarkModeToggle() {
  const [dark, setDark] = useState(false);

  useEffect(() => {
    if (dark) {
      document.body.classList.add("dark-mode");
    } else {
      document.body.classList.remove("dark-mode");
    }
  }, [dark]);

  return (
    <button
      className="darkmode-toggle-btn"
      onClick={() => setDark(!dark)}
      aria-label="Toggle dark mode"
    >
      {dark ? "☀️" : "🌙"}
    </button>
  );
}

export default DarkModeToggle;
