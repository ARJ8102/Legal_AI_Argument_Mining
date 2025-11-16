import type { ReactNode } from "react";
import Navbar from "../components/Navbar";

const AppLayout = ({ children }: { children: ReactNode }) => {
  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-950 text-gray-900 dark:text-gray-100">
      <Navbar />
      <main className="p-6 max-w-6xl mx-auto">{children}</main>
    </div>
  );
};

export default AppLayout;
