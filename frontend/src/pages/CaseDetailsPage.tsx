import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";
import { FaTag, FaQuoteRight } from "react-icons/fa";

const CaseDetailsPage = () => {
  const { id } = useParams();
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    axios.get(`http://127.0.0.1:8000/cases/${id}`).then((res) => {
      setData(res.data.case);
    });
  }, [id]);

  if (!data) {
    return <p className="text-gray-300 text-center mt-10">Loading case details...</p>;
  }

  return (
    <div className="max-w-4xl mx-auto space-y-10">

      {/* HEADER */}
      <div className="bg-gray-900 p-6 rounded-xl shadow-lg">
        <h1 className="text-3xl font-bold text-white">{data.filename}</h1>
        <p className="text-gray-400 mt-2">Case ID: {data.doc_id}</p>
      </div>

      {/* ENTITIES */}
      <section>
        <h2 className="text-2xl font-semibold text-white mb-3">Named Entities</h2>

        <div className="bg-gray-800 p-5 rounded-xl shadow-lg space-y-3">
          {data.entities.length === 0 ? (
            <p className="text-gray-400">No entities detected.</p>
          ) : (
            data.entities.map((e: any, i: number) => (
              <span
                key={i}
                className="inline-block bg-green-700 text-white px-3 py-1 rounded-full text-sm mr-2 mb-2"
              >
                <FaTag className="inline mr-1" />
                {e.entity_group}: {e.word}
              </span>
            ))
          )}
        </div>
      </section>

      {/* ARGUMENT CLASSIFICATIONS */}
      <section>
        <h2 className="text-2xl font-semibold text-white mb-3">Argument Classification</h2>

        <div className="bg-gray-800 p-5 rounded-xl shadow-lg space-y-4">
          {data.classifications.length === 0 ? (
            <p className="text-gray-400">No classified sentences found.</p>
          ) : (
            data.classifications.map((c: any, i: number) => (
              <div
                key={i}
                className="p-4 border border-gray-700 rounded-lg bg-gray-900 shadow"
              >
                <p className="font-semibold text-white">
                  <FaQuoteRight className="inline mr-2 text-blue-400" />
                  {c.sentence}
                </p>

                <p className="text-blue-400 mt-1">→ {c.label}</p>
              </div>
            ))
          )}
        </div>
      </section>
    </div>
  );
};

export default CaseDetailsPage;

