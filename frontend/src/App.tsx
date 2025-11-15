import { useState } from "react";
import axios from "axios";
import { FaFilePdf, FaTag } from "react-icons/fa";

function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleUpload = async () => {
    if (!selectedFile) {
      setError("Please select a PDF before uploading.");
      return;
    }

    setLoading(true);
    setResults(null);
    setError(null);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/process_pdf",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );

      if (response.data.status === "error") {
        setError(response.data.message);
      } else {
        setResults(response.data.results);
      }
    } catch (err) {
      console.error(err);
      setError("Upload failed — check backend connection.");
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-[#0A0F1F] text-gray-200 p-10 font-sans">

      {/* HEADER */}
      <h1 className="text-4xl font-bold mb-6 text-center text-white tracking-wide">
        Legal AI · Document Analyzer
      </h1>

      {/* UPLOAD CARD */}
      <div className="bg-[#131A2A] p-8 rounded-xl shadow-xl max-w-xl mx-auto border border-[#1f2a44]">
        <label className="block mb-4 text-gray-300 font-medium">
          Upload a PDF Document
        </label>

        <div className="flex items-center justify-center bg-[#0F1626] border border-gray-600 rounded-lg py-6 mb-4 cursor-pointer hover:border-gray-400 transition">
          <input
            type="file"
            accept="application/pdf"
            className="opacity-0 absolute h-20 w-80 cursor-pointer"
            onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
          />
          <div className="flex flex-col items-center">
            <FaFilePdf size={34} className="text-red-500 mb-2" />
            <p className="text-gray-400">
              {selectedFile ? selectedFile.name : "Click to choose a PDF"}
            </p>
          </div>
        </div>

        <button
          onClick={handleUpload}
          disabled={loading}
          className="w-full bg-[#D8232A] py-3 rounded-md text-white font-semibold text-lg hover:bg-red-700 disabled:bg-gray-600 transition"
        >
          {loading ? "Analyzing..." : "Upload & Analyze"}
        </button>
      </div>

      {/* ERROR MESSAGE */}
      {error && (
        <div className="max-w-xl mx-auto mt-6 p-4 bg-red-800/40 border border-red-600 rounded-lg text-red-300">
          ⚠ {error}
        </div>
      )}

      {/* FULL SCREEN LOADING OVERLAY */}
      {loading && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="animate-spin rounded-full h-20 w-20 border-t-4 border-red-500 border-opacity-75"></div>
        </div>
      )}

      {/* RESULTS */}
      {results && (
        <div className="mt-12 max-w-5xl mx-auto space-y-10">

          {/* ENTITIES SECTION */}
          <div className="bg-[#131A2A] p-8 rounded-xl shadow-xl border border-[#1f2a44]">
            <h2 className="text-2xl font-bold text-white mb-4">
              Named Entities
            </h2>

            <div className="space-y-3 max-h-80 overflow-auto pr-2">
              {!results.entities || results.entities.length === 0 ? (
                <p className="text-gray-400 text-center">No entities detected.</p>
              ) : (
                results.entities.map((e: any, i: number) => (
                  <div
                    key={i}
                    className="flex items-center justify-between bg-[#0F1626] p-4 rounded-lg border border-gray-700 hover:border-gray-500 transition"
                  >
                    <div>
                      <p className="text-lg font-semibold text-white">{e.word}</p>
                      <p className="text-sm text-gray-400">Position: {e.start}–{e.end}</p>
                    </div>

                    <span className="px-3 py-1 text-sm bg-red-700/40 border border-red-600 rounded-md text-red-300 flex items-center gap-2">
                      <FaTag /> {e.entity_group}
                    </span>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* ARGUMENTS SECTION */}
          <div className="bg-[#131A2A] p-8 rounded-xl shadow-xl border border-[#1f2a44]">
            <h2 className="text-2xl font-bold text-white mb-4">
              Argument Classification
            </h2>

            <div className="space-y-4 max-h-[500px] overflow-auto pr-2">
              {!results.classifications ||
              results.classifications.length === 0 ? (
                <p className="text-gray-400 text-center">
                  No argument classifications returned.
                </p>
              ) : (
                results.classifications.map((c: any, i: number) => (
                  <div
                    key={i}
                    className="bg-[#0F1626] p-5 rounded-lg border border-gray-700 hover:border-gray-500 transition"
                  >
                    <p className="text-white font-semibold mb-1">{c.sentence}</p>
                    <p className="text-sm text-red-400">→ {c.label}</p>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
