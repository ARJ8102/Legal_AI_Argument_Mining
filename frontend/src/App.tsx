import { useState } from "react";
import axios from "axios";

function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any>(null);

  const handleUpload = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setResults(null);

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

      // Back-end sends: { status, filename, results }
      setResults(response.data.results);
    } catch (err) {
      console.error(err);
      alert("Error uploading PDF");
    }

    setLoading(false);
  };

  return (
    <div className="relative min-h-screen bg-gray-900 text-white p-10">

      {/* 🔥 FULLSCREEN LOADING OVERLAY */}
      {loading && (
        <div className="absolute inset-0 bg-black/60 backdrop-blur-sm flex flex-col items-center justify-center z-50">
          <div className="w-16 h-16 border-4 border-blue-400 border-t-transparent rounded-full animate-spin" />
          <p className="mt-4 text-lg font-semibold">Processing PDF…</p>
        </div>
      )}

      <h1 className="text-4xl font-bold mb-6 text-center">
        Legal AI Document Analyzer
      </h1>

      {/* Upload Section */}
      <div
        className={`bg-gray-800 p-6 rounded-xl shadow-lg max-w-xl mx-auto ${
          loading ? "opacity-50 pointer-events-none" : ""
        }`}
      >
        <input
          type="file"
          accept="application/pdf"
          className="block mb-4"
          onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
        />

        <button
          onClick={handleUpload}
          disabled={loading}
          className="bg-blue-600 px-5 py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-600"
        >
          {loading ? "Processing..." : "Upload & Process"}
        </button>
      </div>

      {/* Results Section */}
{results && (
  <div className="mt-10 bg-gray-800 p-6 rounded-xl shadow-xl max-w-4xl mx-auto">
    <h2 className="text-2xl font-semibold mb-4">Results</h2>

    {/* Entities */}
    <h3 className="text-xl font-bold mt-4 mb-2">Named Entities</h3>
    <div className="bg-gray-700 p-4 rounded-md overflow-auto max-h-60">
      {!results.entities || results.entities.length === 0 ? (
        <p>No entities found.</p>
      ) : (
        results.entities.map((e: any, i: number) => (
          <p key={i} className="mb-1">
            <span className="text-green-400">{e.entity_group}</span>
            {": "}
            {e.word}
          </p>
        ))
      )}
    </div>

    {/* Arguments */}
    <h3 className="text-xl font-bold mt-6 mb-2">Arguments</h3>
    <div className="bg-gray-700 p-4 rounded-md overflow-auto max-h-80">
      {!results.classifications || results.classifications.length === 0 ? (
        <p>No argument classifications found.</p>
      ) : (
        results.classifications.map((c: any, i: number) => (
          <div key={i} className="mb-3">
            <p className="font-semibold">{c.sentence}</p>
            <p className="text-blue-300">→ {c.label}</p>
          </div>
        ))
      )}
    </div>
  </div>
)}

    </div>
  );
}

export default App;
