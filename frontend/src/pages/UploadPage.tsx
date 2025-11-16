import { useState } from "react";
import axios from "axios";
import { motion } from "framer-motion";
import { FaCloudUploadAlt, FaCheckCircle } from "react-icons/fa";

const UploadPage = () => {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<"idle" | "uploading" | "success" | "error">(
    "idle"
  );
  const [message, setMessage] = useState("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0] || null;
    setFile(f);
    setStatus("idle");
    setMessage("");
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    try {
      setStatus("uploading");
      setMessage("");

      const formData = new FormData();
      formData.append("file", file);

      const res = await axios.post("http://127.0.0.1:8000/process_pdf", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      if (res.data.status === "success") {
        setStatus("success");
        setMessage(`Processed: ${res.data.filename} (ID: ${res.data.doc_id})`);
      } else {
        setStatus("error");
        setMessage(res.data.message || "Processing failed.");
      }
    } catch (err: any) {
      setStatus("error");
      setMessage(err?.message || "Unexpected error");
    }
  };

  return (
    <div className="max-w-3xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-slate-900/90 border border-slate-700 rounded-2xl p-8 shadow-2xl"
      >
        <h1 className="text-3xl font-bold text-white mb-2">Upload a Legal Case</h1>
        <p className="text-slate-300 mb-6 text-sm">
          Upload a PDF judgment or legal document. We’ll extract entities and
          classify arguments automatically.
        </p>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* File picker card */}
          <label className="flex flex-col items-center justify-center border-2 border-dashed border-slate-600 rounded-2xl px-6 py-10 cursor-pointer hover:border-indigo-500 hover:bg-slate-800/60 transition">
            <FaCloudUploadAlt className="text-4xl text-indigo-400 mb-3" />
            <span className="text-white font-medium">
              {file ? file.name : "Click to choose a PDF file"}
            </span>
            <span className="text-xs text-slate-400 mt-1">
              Supported: .pdf • Max ~10–20MB recommended
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
            className="w-full py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-600 text-white font-semibold shadow-lg transition flex items-center justify-center gap-2"
          >
            {status === "uploading" ? (
              <>
                <span className="h-4 w-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                Processing…
              </>
            ) : (
              "Process PDF"
            )}
          </button>
        </form>

        {/* Status message */}
        {status !== "idle" && (
          <div className="mt-5">
            {status === "success" && (
              <div className="flex items-center gap-2 text-emerald-400">
                <FaCheckCircle />
                <p className="text-sm">{message}</p>
              </div>
            )}
            {status === "error" && (
              <p className="text-sm text-red-400">⚠ {message}</p>
            )}
          </div>
        )}
      </motion.div>
    </div>
  );
};

export default UploadPage;
