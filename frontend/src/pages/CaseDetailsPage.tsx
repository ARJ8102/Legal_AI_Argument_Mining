import { useParams } from "react-router-dom";
import { useEffect, useState, useMemo } from "react";
import axios from "axios";
import { FaTag, FaQuoteRight } from "react-icons/fa";

const entityColorMap: Record<string, string> = {
  PERSON: "bg-emerald-700",
  ORG: "bg-indigo-700",
  LOC: "bg-blue-700",
  GPE: "bg-orange-600",
  LAW: "bg-fuchsia-700",
};

const labelColorMap: Record<string, string> = {
  UNKNOWN: "bg-slate-700",
  CLAIM: "bg-indigo-700",
  PREMISE: "bg-emerald-700",
  COUNTER: "bg-rose-700",
};

const CaseDetailsPage = () => {
  const { id } = useParams();
  const [data, setData] = useState<any>(null);
  const [search, setSearch] = useState("");

  useEffect(() => {
    axios.get(`http://127.0.0.1:8000/cases/${id}`).then((res) => {
      setData(res.data.case);
    });
  }, [id]);

  const filteredClassifications = useMemo(() => {
    if (!data?.classifications) return [];
    if (!search.trim()) return data.classifications;
    const q = search.toLowerCase();
    return data.classifications.filter((c: any) =>
      c.sentence.toLowerCase().includes(q)
    );
  }, [data, search]);

  if (!data) {
    return <p className="text-gray-300 text-center mt-10">Loading case details...</p>;
  }

  return (
    <div className="max-w-5xl mx-auto space-y-10">
      {/* HEADER */}
      <div className="bg-slate-900 border border-slate-700 p-6 rounded-2xl shadow-lg">
        <h1 className="text-3xl font-bold text-white mb-2">{data.filename}</h1>
        <p className="text-slate-400 text-sm">Case ID: {data.doc_id}</p>
      </div>

      {/* ENTITIES */}
      <section className="space-y-3">
        <h2 className="text-2xl font-semibold text-white">Named Entities</h2>
        <div className="bg-slate-900 border border-slate-700 p-5 rounded-2xl shadow-lg">
          {(!data.entities || data.entities.length === 0) && (
            <p className="text-slate-400 text-sm">No entities detected.</p>
          )}

          <div className="flex flex-wrap gap-2">
            {data.entities?.map((e: any, i: number) => {
              const cls =
                entityColorMap[e.entity_group] || "bg-slate-700";
              return (
                <span
                  key={i}
                  className={`${cls} inline-flex items-center gap-1 text-xs px-3 py-1 rounded-full text-white`}
                >
                  <FaTag className="text-xs opacity-80" />
                  <span className="font-semibold">{e.entity_group}</span>
                  <span className="opacity-90">· {e.word}</span>
                </span>
              );
            })}
          </div>
        </div>
      </section>

      {/* ARGUMENT CLASSIFICATIONS */}
      <section className="space-y-3">
        <div className="flex items-center justify-between gap-4">
          <h2 className="text-2xl font-semibold text-white">
            Argument Classification
          </h2>
          <input
            type="text"
            placeholder="Filter sentences..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-700 text-sm text-slate-100 placeholder:text-slate-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
          />
        </div>

        <div className="bg-slate-900 border border-slate-700 p-5 rounded-2xl shadow-lg space-y-4 max-h-[550px] overflow-y-auto">
          {filteredClassifications.length === 0 && (
            <p className="text-slate-400 text-sm">No sentences match this filter.</p>
          )}

          {filteredClassifications.map((c: any, i: number) => {
            const labelClass =
              labelColorMap[c.label] || "bg-slate-700";

            return (
              <div
                key={i}
                className="p-4 rounded-xl bg-slate-950/70 border border-slate-700 hover:border-indigo-500 transition group"
              >
                <p className="font-medium text-slate-100">
                  <FaQuoteRight className="inline mr-2 text-indigo-400 group-hover:text-indigo-300" />
                  <span
                    className={
                      search
                        ? "bg-yellow-200/30 text-yellow-100"
                        : ""
                    }
                  >
                    {c.sentence}
                  </span>
                </p>
                <div className="mt-2 flex items-center justify-between">
                  <span
                    className={`${labelClass} inline-block text-xs px-3 py-1 rounded-full text-white font-semibold`}
                  >
                    {c.label}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </section>
    </div>
  );
};

export default CaseDetailsPage;
