import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <div className="bg-gray-900 text-white px-6 py-4 flex justify-between items-center shadow">
      <h1 className="text-xl font-bold text-red-400">Legal AI</h1>

      <div className="flex gap-6">
        <Link to="/" className="hover:text-red-300">Upload</Link>
        <Link to="/cases" className="hover:text-red-300">Cases</Link>
      </div>
    </div>
  );
}
