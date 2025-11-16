import { useEffect, useState, useMemo } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import { FaFolderOpen, FaSearch } from "react-icons/fa";
import { motion } from "framer-motion";

interface CaseItem {
  doc_id: string;
  filename: string;
}

const CasesListPage = () => {
  const [cases, setCases] = useState<CaseItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [query, setQuery] = useState("");

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/cases").then((res) => {
      setCases(res.data.cases);
      setLoading(false);
    });
  }, []);

  const filtered = useMemo(
    () =>
      cases.filter((c) =>
        c.filename.toLowerCase().includes(query.toLowerCase())
      ),
    [cases, query]
  );

  if (loading) {
    return <p className="text-gray-300 text-center mt-10">Loading cases...</p>;
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex items-center justify-between gap-4">
        <h1 className="text-3xl font-bold text-white">Processed Cases</h1>

        <div className="relative">
          <FaSearch className="absolute left-2 top-2.5 text-slate-400 text-sm" />
          <input
            type="text"
            placeholder="Search by filename..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="pl-7 pr-3 py-1.5 rounded-lg bg-slate-900 border border-slate-700 text-sm text-slate-100 placeholder:text-slate-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
          />
        </div>
      </div>

      {filtered.length === 0 && (
        <div className="text-center text-gray-400 mt-20">
          <FaFolderOpen className="mx-auto text-5xl mb-4 opacity-70" />
          <p>No matching cases.</p>
        </div>
      )}

      <div className="space-y-4">
        {filtered.map((c, index) => (
          <motion.div
            key={c.doc_id}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.03 }}
          >
            <Link
              to={`/cases/${c.doc_id}`}
              className="block bg-slate-900 border border-slate-700 hover:border-indigo-500 hover:bg-slate-800 p-4 rounded-xl shadow-md transition"
            >
              <p className="text-lg font-semibold text-white">{c.filename}</p>
              <p className="text-slate-400 text-xs mt-1">
                Case ID: {c.doc_id} • Click to view full analysis
              </p>
            </Link>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default CasesListPage;
