import { useState } from "react";
import axios from "axios";
import { motion } from "framer-motion";
import {
  FaBrain,
  FaCloudUploadAlt,
  FaCheckCircle,
  FaDatabase,
  FaFilePdf,
  FaGavel,
  FaSearch,
  FaServer,
} from "react-icons/fa";

const UploadPage = () => {
  const [file, setFile] = useState<File | null>(null);
  const [docId, setDocId] = useState("");
  const [status, setStatus] = useState<"idle" | "uploading" | "success" | "error">("idle");
  const [message, setMessage] = useState("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0] || null;
    setFile(f);
    setDocId("");
    setStatus("idle");
    setMessage("");
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    try {
      setStatus("uploading");
      setDocId("");
      setMessage("");

      const formData = new FormData();
      formData.append("file", file);

      const res = await axios.post("http://127.0.0.1:8000/process_pdf", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      if (res.data.status === "success") {
        setStatus("success");
        setDocId(res.data.doc_id);
        setMessage(`Processed ${res.data.filename}.`);
      } else {
        setStatus("error");
        setDocId("");
        setMessage(res.data.message || "Processing failed.");
      }
    } catch (err: any) {
      setStatus("error");
      setDocId("");
      setMessage(err?.message || "Unexpected error");
    }
  };

  const features = [
    {
      icon: <FaFilePdf />,
      title: "PDF Intelligence",
      text: "Extracts text from legal PDFs with OCR fallback for scanned documents.",
    },
    {
      icon: <FaSearch />,
      title: "Legal Entity Extraction",
      text: "Identifies people, organizations, locations, courts, and legal references.",
    },
    {
      icon: <FaBrain />,
      title: "Fine-Tuned LegalBERT",
      text: "Classifies sentences into facts, issues, arguments, reasoning, and decisions.",
    },
    {
      icon: <FaServer />,
      title: "Full-Stack AI Pipeline",
      text: "React, FastAPI, MongoDB, PyTorch, Transformers, and Palmetto GPU training.",
    },
  ];

  const pipelineSteps = [
    "PDF Text Extraction",
    "OCR Fallback",
    "Named Entity Recognition",
    "Sentence Segmentation",
    "LegalBERT Role Classification",
    "MongoDB Case Storage",
  ];

  return (
    <div className="max-w-7xl mx-auto">
      <div className="grid lg:grid-cols-[1.1fr_0.9fr] gap-8 items-start">
        <motion.section
          initial={{ opacity: 0, y: 14 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          <div className="inline-flex items-center gap-2 rounded-full border border-indigo-500/40 bg-indigo-500/10 px-4 py-2 text-sm text-indigo-200">
            <FaGavel />
            Legal Document Intelligence Platform
          </div>

          <div>
            <h1 className="text-5xl font-extrabold tracking-tight text-white leading-tight">
              Turn court judgments into structured legal analysis.
            </h1>
            <p className="mt-5 text-lg text-slate-300 max-w-2xl">
              Upload a legal PDF and extract named entities, sentence-level rhetorical
              roles, party arguments, judicial reasoning, and decision segments using a
              fine-tuned InLegalBERT model.
            </p>
          </div>

          <div className="grid sm:grid-cols-3 gap-4">
            <div className="rounded-2xl border border-slate-700 bg-slate-900/80 p-5">
              <p className="text-3xl font-bold text-white">1.5M+</p>
              <p className="text-sm text-slate-400 mt-1">legal sentence annotations</p>
            </div>
            <div className="rounded-2xl border border-slate-700 bg-slate-900/80 p-5">
              <p className="text-3xl font-bold text-white">6</p>
              <p className="text-sm text-slate-400 mt-1">rhetorical role classes</p>
            </div>
            <div className="rounded-2xl border border-slate-700 bg-slate-900/80 p-5">
              <p className="text-3xl font-bold text-white">GPU</p>
              <p className="text-sm text-slate-400 mt-1">trained on Palmetto</p>
            </div>
          </div>

          <div className="grid sm:grid-cols-2 gap-4">
            {features.map((f) => (
              <div
                key={f.title}
                className="rounded-2xl border border-slate-700 bg-slate-900/70 p-5 hover:border-indigo-500/70 transition"
              >
                <div className="text-indigo-300 text-2xl mb-3">{f.icon}</div>
                <h3 className="text-white font-semibold">{f.title}</h3>
                <p className="text-sm text-slate-400 mt-2">{f.text}</p>
              </div>
            ))}
          </div>
        </motion.section>

        <motion.section
          initial={{ opacity: 0, y: 14 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.08 }}
          className="rounded-3xl border border-slate-700 bg-slate-900/90 p-7 shadow-2xl"
        >
          <div className="flex items-center gap-3 mb-6">
            <div className="h-11 w-11 rounded-2xl bg-indigo-500/20 flex items-center justify-center text-indigo-300">
              <FaCloudUploadAlt size={22} />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-white">Analyze a Legal PDF</h2>
              <p className="text-sm text-slate-400">Upload a judgment or legal document.</p>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="space-y-5">
            <label className="flex flex-col items-center justify-center border-2 border-dashed border-slate-600 rounded-2xl px-6 py-12 cursor-pointer hover:border-indigo-500 hover:bg-slate-800/60 transition">
              <FaCloudUploadAlt className="text-5xl text-indigo-400 mb-4" />
              <span className="text-white font-semibold text-center">
                {file ? file.name : "Drop your PDF here or click to browse"}
              </span>
              <span className="text-xs text-slate-400 mt-2">
                Supported: PDF · Recommended size: 10–20 MB
              </span>
              <input
                type="file"
                accept="application/pdf"
                className="hidden"
                onChange={handleFileChange}
              />
            </label>

            <button
              type="submit"
              disabled={!file || status === "uploading"}
              className="w-full py-3.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-700 disabled:text-slate-400 text-white font-semibold transition flex items-center justify-center gap-2"
            >
              {status === "uploading" ? (
                <>
                  <span className="h-4 w-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Processing with AI pipeline...
                </>
              ) : (
                "Run Legal Analysis"
              )}
            </button>
          </form>

          {status !== "idle" && (
            <div className="mt-5 rounded-xl border border-slate-700 bg-slate-950 p-4">
              {status === "success" && (
                <div className="space-y-3">
                  <div className="flex items-center gap-2 text-emerald-400">
                    <FaCheckCircle />
                    <p className="text-sm">{message}</p>
                  </div>

                  {docId && (
                    <a
                      href={`/cases/${docId}`}
                      className="block text-center rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-semibold py-2.5 transition"
                    >
                      Open Legal Analysis
                    </a>
                  )}
                </div>
              )}

              {status === "error" && <p className="text-sm text-red-400">{message}</p>}

              {status === "uploading" && (
                <p className="text-sm text-slate-300">
                  Extracting text, running NER, and classifying legal roles. First model load may take a moment.
                </p>
              )}
            </div>
          )}

          <div className="mt-6 flex items-center gap-2 text-xs text-slate-500">
            <FaDatabase />
            Results are stored in MongoDB and shown in the Cases dashboard.
          </div>

          <div className="mt-6 rounded-2xl border border-slate-700 bg-slate-950/70 p-5">
            <h3 className="text-white font-semibold mb-4">Analysis Pipeline</h3>

            <div className="space-y-4">
              {pipelineSteps.map((step, index) => (
                <div key={step} className="flex items-center gap-3">
                  <div className="h-7 w-7 rounded-full bg-indigo-500/20 text-indigo-300 flex items-center justify-center text-xs font-bold">
                    {index + 1}
                  </div>
                  <p className="text-sm text-slate-300">{step}</p>
                </div>
              ))}
            </div>
          </div>
        </motion.section>
      </div>
    </div>
  );
};

export default UploadPage;