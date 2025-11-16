import { useEffect, useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

interface CaseItem {
  doc_id: string;
  filename: string;
}

const CasesListPage = () => {
  const [cases, setCases] = useState<CaseItem[]>([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/cases").then((res) => {
      setCases(res.data.cases);
    });
  }, []);

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6 text-white">Processed Cases</h1>

      {cases.length === 0 && <p>No cases processed yet.</p>}

      <div className="space-y-4">
        {cases.map((c) => (
          <Link
            key={c.doc_id}
            to={`/cases/${c.doc_id}`}
            className="block bg-gray-800 hover:bg-gray-700 p-4 rounded-lg"
          >
            {c.filename}
          </Link>
        ))}
      </div>
    </div>
  );
};

export default CasesListPage;
