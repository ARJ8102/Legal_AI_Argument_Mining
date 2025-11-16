import type { ReactNode } from "react";
import { Link, NavLink } from "react-router-dom";
import { useTheme } from "../context/ThemeContext";
import { FaMoon, FaSun, FaBalanceScale } from "react-icons/fa";

const navLinkBase =
  "px-3 py-2 rounded-lg text-sm font-medium transition-colors";
const navLinkActive = "bg-indigo-600 text-white";
const navLinkInactive =
  "text-gray-300 hover:bg-gray-700 hover:text-white dark:text-gray-300";

export const Layout = ({ children }: { children: ReactNode }) => {
  const { theme, toggleTheme } = useTheme();

  return (
    <div className="min-h-screen bg-slate-100 text-slate-900 dark:bg-slate-950 dark:text-slate-100">
      {/* NAVBAR */}
      <header className="border-b border-slate-200/10 bg-slate-900/80 backdrop-blur sticky top-0 z-20">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
          {/* Brand */}
          <Link to="/" className="flex items-center gap-2">
            <div className="h-9 w-9 rounded-xl bg-indigo-600 flex items-center justify-center shadow-lg">
              <FaBalanceScale className="text-white" />
            </div>
            <div className="leading-tight">
              <p className="font-semibold text-white text-sm md:text-base">
                Legal AI
              </p>
              <p className="text-xs text-slate-300">
                Argument Mining Dashboard
              </p>
            </div>
          </Link>

          {/* Nav + Theme */}
          <div className="flex items-center gap-3">
            <nav className="hidden sm:flex gap-1">
              <NavLink
                to="/"
                className={({ isActive }) =>
                  `${navLinkBase} ${
                    isActive ? navLinkActive : navLinkInactive
                  }`
                }
              >
                Dashboard
              </NavLink>
              <NavLink
                to="/upload"
                className={({ isActive }) =>
                  `${navLinkBase} ${
                    isActive ? navLinkActive : navLinkInactive
                  }`
                }
              >
                Upload
              </NavLink>
              <NavLink
                to="/cases"
                className={({ isActive }) =>
                  `${navLinkBase} ${
                    isActive ? navLinkActive : navLinkInactive
                  }`
                }
              >
                Cases
              </NavLink>
            </nav>

            {/* Dark mode toggle */}
            <button
              onClick={toggleTheme}
              className="ml-1 inline-flex items-center justify-center h-9 w-9 rounded-full border border-slate-600 bg-slate-800 text-yellow-300 hover:bg-slate-700 transition"
              aria-label="Toggle dark mode"
            >
              {theme === "dark" ? <FaSun /> : <FaMoon />}
            </button>
          </div>
        </div>
      </header>

      {/* MAIN CONTENT */}
      <main className="max-w-6xl mx-auto px-4 py-6">{children}</main>
    </div>
  );
};
