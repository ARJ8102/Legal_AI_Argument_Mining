import { useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

const UploadPage = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please select a PDF first");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      await axios.post("http://127.0.0.1:8000/process_pdf", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      alert("File processed. Check the Cases page.");
    } catch (err) {
      console.error(err);
      alert("Upload failed.");
    }

    setLoading(false);
  };

  return (
    <div className="text-center mt-20">
      <input
        type="file"
        accept="application/pdf"
        onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
        className="block mx-auto mb-4"
      />

      <button
        onClick={handleUpload}
        disabled={loading}
        className="bg-red-600 px-6 py-3 rounded-lg text-white hover:bg-red-700 disabled:bg-gray-600"
      >
        {loading ? "Processing..." : "Upload & Process"}
      </button>

      <Link
        to="/cases"
        className="text-blue-300 hover:underline block mt-6 text-lg"
      >
        View Processed Cases →
      </Link>
    </div>
  );
};

export default UploadPage;
