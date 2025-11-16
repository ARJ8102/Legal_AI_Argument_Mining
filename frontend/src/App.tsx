import { Routes, Route } from "react-router-dom";
import AppLayout from "./Layout/AppLayout";
import UploadPage from "./pages/UploadPage";
import CasesListPage from "./pages/CasesListPage";
import CaseDetailsPage from "./pages/CaseDetailsPage";

const App = () => {
  return (
    <AppLayout>
      <Routes>
        <Route path="/" element={<UploadPage />} />
        <Route path="/upload" element={<UploadPage />} />
        <Route path="/cases" element={<CasesListPage />} />
        <Route path="/cases/:id" element={<CaseDetailsPage />} />
      </Routes>
    </AppLayout>
  );
};

export default App;
