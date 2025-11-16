import { Routes, Route } from "react-router-dom";

import UploadPage from "./pages/UploadPage";
import CasesListPage from "./pages/CasesListPage";
import CaseDetailsPage from "./pages/CaseDetailsPage";

import Navbar from "./components/Navbar";

function App() {
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <Navbar />

      <div className="p-6">
        <Routes>
          <Route path="/" element={<UploadPage />} />
          <Route path="/upload" element={<UploadPage />} />
          <Route path="/cases" element={<CasesListPage />} />
          <Route path="/cases/:id" element={<CaseDetailsPage />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
