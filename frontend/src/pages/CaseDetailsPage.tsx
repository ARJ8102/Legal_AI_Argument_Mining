import { useParams } from "react-router-dom";
import { useEffect, useState, useMemo } from "react";
import axios from "axios";
import { FaTag, FaQuoteRight } from "react-icons/fa";

const CaseDetailsPage = () => {
  const { id } = useParams();
  const [data, setData] = useState<any>(null);
  const [search, setSearch] = useState("");

  useEffect(() => {
    axios.get(`http://127.0.0.1:8000/cases/${id}`).then((res) => {
      setData(res.data.case);
    });
  }, [id]);

  const classifications = data?.classifications?.items || [];
  const grouped = data?.classifications?.labels || {};

  const filtered = useMemo(() => {
    if (!search.trim()) return classifications;
    const q = search.toLowerCase();
    return classifications.filter((c: any) =>
      c.sentence.toLowerCase().includes(q)
    );
  }, [classifications, search]);

  if (!data) return <p className="text-center text-slate-300 mt-10">Loading...</p>;

  const sections = [
    "Facts",
    "Issue",
    "Arguments of Petitioner",
    "Arguments of Respondent",
    "Reasoning",
    "Decision",
  ];

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div className="bg-slate-900 border border-slate-700 p-6 rounded-2xl">
        <h1 className="text-3xl font-bold text-white">{data.filename}</h1>
        <p className="text-slate-400 mt-2">Case ID: {data.doc_id}</p>

        <div className="grid grid-cols-3 gap-4 mt-5">
          <div className="bg-slate-950 p-4 rounded-xl">
            <p className="text-slate-400 text-sm">Entities</p>
            <p className="text-white text-2xl font-bold">{data.entities?.length || 0}</p>
          </div>
          <div className="bg-slate-950 p-4 rounded-xl">
            <p className="text-slate-400 text-sm">Total Sentences</p>
            <p className="text-white text-2xl font-bold">{data.classifications?.total_sentences || 0}</p>
          </div>
          <div className="bg-slate-950 p-4 rounded-xl">
            <p className="text-slate-400 text-sm">Classified</p>
            <p className="text-white text-2xl font-bold">{data.classifications?.classified_count || 0}</p>
          </div>
        </div>
      </div>

      <section>
        <h2 className="text-2xl font-semibold text-white mb-3">Named Entities</h2>
        <div className="bg-slate-900 border border-slate-700 p-5 rounded-2xl flex flex-wrap gap-2">
          {data.entities?.map((e: any, i: number) => (
            <span key={i} className="bg-indigo-700 text-white text-xs px-3 py-1 rounded-full">
              <FaTag className="inline mr-1" />
              {e.entity_group} · {e.word}
            </span>
          ))}
        </div>
      </section>

      <section>
        <div className="flex justify-between mb-3">
          <h2 className="text-2xl font-semibold text-white">Legal Rhetorical Role Analysis</h2>
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search sentences..."
            className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white"
          />
        </div>

        {search ? (
          <div className="bg-slate-900 border border-slate-700 p-5 rounded-2xl space-y-3">
            {filtered.map((c: any, i: number) => (
              <div key={i} className="bg-slate-950 p-4 rounded-xl border border-slate-700">
                <p className="text-slate-100">
                  <FaQuoteRight className="inline mr-2 text-indigo-400" />
                  {c.sentence}
                </p>
                <p className="text-xs text-indigo-300 mt-2">
                  {c.label} · confidence {c.score}
                </p>
              </div>
            ))}
          </div>
        ) : (
          <div className="space-y-6">
            {sections.map((label) => (
              <div key={label} className="bg-slate-900 border border-slate-700 p-5 rounded-2xl">
                <h3 className="text-xl font-bold text-white mb-3">
                  {label} <span className="text-slate-400 text-sm">({grouped[label]?.length || 0})</span>
                </h3>

                <div className="space-y-3 max-h-80 overflow-y-auto">
                  {(grouped[label] || []).slice(0, 15).map((c: any, i: number) => (
                    <div key={i} className="bg-slate-950 p-4 rounded-xl border border-slate-700">
                      <p className="text-slate-100">{c.sentence}</p>
                      <p className="text-xs text-indigo-300 mt-2">Confidence: {c.score}</p>
                    </div>
                  ))}

                  {!grouped[label]?.length && (
                    <p className="text-slate-400 text-sm">No sentences found.</p>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
};

export default CaseDetailsPage;