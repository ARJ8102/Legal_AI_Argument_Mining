import { Link } from "react-router-dom";
import { useTheme } from "../context/ThemeContext";
import { FaSun, FaMoon, FaFileUpload, FaList } from "react-icons/fa";

const Navbar = () => {
  const { theme, toggleTheme } = useTheme();

  return (
    <nav className="w-full bg-gray-900 dark:bg-black px-6 py-4 shadow-md flex justify-between items-center">
      <Link to="/" className="text-2xl font-bold text-white">
        Legal AI
      </Link>

      <div className="flex items-center gap-6">
        <Link to="/upload" className="text-gray-300 hover:text-white flex items-center gap-2">
          <FaFileUpload /> Upload
        </Link>

        <Link to="/cases" className="text-gray-300 hover:text-white flex items-center gap-2">
          <FaList /> Cases
        </Link>

        <button
          onClick={toggleTheme}
          className="text-gray-300 hover:text-white"
        >
          {theme === "light" ? <FaMoon size={18} /> : <FaSun size={18} />}
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
