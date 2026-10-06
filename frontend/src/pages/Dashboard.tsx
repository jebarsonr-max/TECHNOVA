import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Database, Cpu, History, ArrowRight, Sparkles, CheckCircle2, AlertTriangle, ShieldCheck } from 'lucide-react';
import { apiService } from '../services/api';
import { Dataset, Analysis, DemoQuestion } from '../types';
import { UploadZone } from '../components/UploadZone';
import { DatasetCard } from '../components/DatasetCard';
import { LoadingState } from '../components/States';

export const DashboardPage: React.FC = () => {
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [recentAnalyses, setRecentAnalyses] = useState<Analysis[]>([]);
  const [demoQuestions, setDemoQuestions] = useState<DemoQuestion[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    setLoading(true);
    try {
      const [ds, history, questions] = await Promise.all([
        apiService.getDatasets(),
        apiService.getAnalysisHistory(),
        apiService.getDemoQuestions(),
      ]);
      setDatasets(ds);
      setRecentAnalyses(history.slice(0, 5));
      setDemoQuestions(questions);
    } catch (err) {
      console.error('Failed to load dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDatasetUploaded = (newDs: Dataset) => {
    setDatasets((prev) => [newDs, ...prev]);
  };

  const handleRunDemoQuestion = async (q: DemoQuestion) => {
    if (datasets.length === 0) {
      alert('Please upload a dataset or wait for datasets to load first.');
      return;
    }
    const targetDs = datasets[0];
    try {
      const analysis = await apiService.createAnalysis(q.question, [targetDs.id]);
      navigate(`/proof/${analysis.id}`);
    } catch (err) {
      alert('Failed to execute analysis question.');
    }
  };

  if (loading) return <LoadingState label="Loading Analytics Studio..." />;

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <Cpu className="w-6 h-6 text-cyan-400" />
            <span>Analytics Studio</span>
          </h1>
          <p className="text-xs text-slate-400">Proof-Carrying AI Data Analysis Workspace</p>
        </div>

        <div className="flex items-center gap-2 text-xs">
          <span className="px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 font-mono">
            {datasets.length} Active Datasets
          </span>
          <span className="px-3 py-1.5 rounded-xl bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 font-semibold">
            Sandbox Active
          </span>
        </div>
      </div>

      {/* Upload Zone */}
      <UploadZone onDatasetUploaded={handleDatasetUploaded} />

      {/* Demo Questions Section */}
      {demoQuestions.length > 0 && (
        <div className="glass-card rounded-2xl p-6 border border-slate-800 space-y-4">
          <div className="flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-cyan-400" />
            <h3 className="font-semibold text-slate-100">Live PS08 Demonstration Questions</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 text-xs">
            {demoQuestions.map((q, idx) => (
              <button
                key={idx}
                onClick={() => handleRunDemoQuestion(q)}
                className="p-4 rounded-xl bg-slate-900/60 hover:bg-slate-900 border border-slate-800 hover:border-cyan-500/40 text-left transition-all space-y-2 group"
              >
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-cyan-400 text-[11px] uppercase tracking-wider">{q.category}</span>
                  <span className={`px-2 py-0.5 rounded text-[10px] font-semibold ${q.expected_status === 'VERIFIED' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'}`}>
                    {q.expected_status}
                  </span>
                </div>
                <p className="font-medium text-slate-200 group-hover:text-cyan-300">{q.question}</p>
                {q.note && <p className="text-[10px] text-slate-500 italic">{q.note}</p>}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Datasets Section */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="font-semibold text-slate-100 flex items-center gap-2">
            <Database className="w-4 h-4 text-teal-400" />
            <span>Uploaded Datasets</span>
          </h3>
          <Link to="/datasets" className="text-xs text-cyan-400 hover:underline flex items-center gap-1">
            <span>View All</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        {datasets.length === 0 ? (
          <div className="p-8 glass-card rounded-2xl border border-slate-800 text-center text-xs text-slate-400">
            No datasets uploaded yet. Drag & drop a CSV file above to start!
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {datasets.slice(0, 3).map((ds) => (
              <DatasetCard key={ds.id} dataset={ds} />
            ))}
          </div>
        )}
      </div>

      {/* Recent Analysis History */}
      {recentAnalyses.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="font-semibold text-slate-100 flex items-center gap-2">
              <History className="w-4 h-4 text-indigo-400" />
              <span>Recent Analyses</span>
            </h3>
            <Link to="/history" className="text-xs text-indigo-400 hover:underline flex items-center gap-1">
              <span>View History</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="space-y-2">
            {recentAnalyses.map((an) => (
              <Link
                key={an.id}
                to={`/proof/${an.id}`}
                className="flex items-center justify-between p-4 rounded-xl glass-card hover:border-cyan-500/40 text-xs transition-all"
              >
                <div className="flex items-center gap-3">
                  <ShieldCheck className="w-4 h-4 text-cyan-400" />
                  <div>
                    <p className="font-semibold text-slate-200">{an.question}</p>
                    <span className="text-slate-500">{new Date(an.created_at).toLocaleString()}</span>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <span className={`font-mono font-semibold ${an.verification_status === 'VERIFIED' ? 'text-emerald-400' : 'text-amber-400'}`}>
                    {an.final_answer}
                  </span>
                  <ArrowRight className="w-4 h-4 text-slate-500" />
                </div>
              </Link>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
