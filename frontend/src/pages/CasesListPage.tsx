import { useEffect, useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import { FaFolderOpen } from "react-icons/fa";

interface CaseItem {
  doc_id: string;
  filename: string;
}

const CasesListPage = () => {
  const [cases, setCases] = useState<CaseItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/cases").then((res) => {
      setCases(res.data.cases);
      setLoading(false);
    });
  }, []);

  if (loading) {
    return <p className="text-gray-300 text-center mt-10">Loading cases...</p>;
  }

  return (
    <div className="max-w-3xl mx-auto">

      <h1 className="text-3xl font-bold mb-6 text-white">
        📁 Processed Cases
      </h1>

      {cases.length === 0 && (
        <div className="text-center text-gray-400 mt-20">
          <FaFolderOpen className="mx-auto text-5xl mb-4 opacity-70" />
          <p>No cases processed yet.</p>
        </div>
      )}

      <div className="space-y-4">
        {cases.map((c) => (
          <Link
            key={c.doc_id}
            to={`/cases/${c.doc_id}`}
            className="block bg-gray-800 p-5 rounded-xl shadow-md hover:shadow-lg hover:bg-gray-700 transition-all"
          >
            <p className="text-xl font-semibold text-white">{c.filename}</p>
            <p className="text-gray-400 text-sm mt-1">
              Click to view complete NLP analysis →
            </p>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default CasesListPage;
