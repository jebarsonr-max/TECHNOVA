import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Navbar } from './components/Navbar';
import { Sidebar } from './components/Sidebar';
import { LandingPage } from './pages/Landing';
import { DashboardPage } from './pages/Dashboard';
import { DatasetsPage } from './pages/Datasets';
import { DatasetDetailPage } from './pages/DatasetDetail';
import { AnalyzePage } from './pages/Analyze';
import { ProofViewPage } from './pages/ProofView';
import { HistoryPage } from './pages/History';
import { SettingsPage } from './pages/Settings';

export const App: React.FC = () => {
  return (
    <Router>
      <div className="min-h-screen flex flex-col bg-[#090d16] text-slate-100 font-sans">
        <Navbar />

        <div className="flex-1 flex max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 gap-6">
          <Sidebar />

          <main className="flex-1 overflow-x-hidden min-w-0">
            <Routes>
              <Route path="/" element={<LandingPage />} />
              <Route path="/dashboard" element={<DashboardPage />} />
              <Route path="/datasets" element={<DatasetsPage />} />
              <Route path="/datasets/:id" element={<DatasetDetailPage />} />
              <Route path="/analyze" element={<AnalyzePage />} />
              <Route path="/analyze/:datasetId" element={<AnalyzePage />} />
              <Route path="/proof/:analysisId" element={<ProofViewPage />} />
              <Route path="/history" element={<HistoryPage />} />
              <Route path="/settings" element={<SettingsPage />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
};

export default App;
