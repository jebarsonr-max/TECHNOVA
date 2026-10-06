import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ShieldCheck, Download, ArrowLeft, Cpu, AlertTriangle } from 'lucide-react';
import { apiService } from '../services/api';
import { Analysis } from '../types';
import { AnswerCard } from '../components/AnswerCard';
import { ProofCard } from '../components/ProofCard';
import { EvidencePanel } from '../components/EvidencePanel';
import { AnalysisTimeline } from '../components/AnalysisTimeline';
import { LoadingState, ErrorState } from '../components/States';

export const ProofViewPage: React.FC = () => {
  const { analysisId } = useParams<{ analysisId: string }>();
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (analysisId) {
      apiService
        .getAnalysis(analysisId)
        .then(setAnalysis)
        .catch((err) => setError(err.message))
        .finally(() => setLoading(false));
    }
  }, [analysisId]);

  const handleDownloadReport = async () => {
    if (!analysisId) return;
    try {
      const reportData = await apiService.getReport(analysisId);
      const jsonStr = JSON.stringify(reportData, null, 2);
      const blob = new Blob([jsonStr], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `TECHNOVA_Proof_Report_${analysisId.slice(0, 8)}.json`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      alert('Failed to download report.');
    }
  };

  if (loading) return <LoadingState label="Verifying proof bundle..." />;
  if (error || !analysis) return <ErrorState message={error || 'Analysis proof not found'} />;

  return (
    <div className="space-y-8">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <Link to="/dashboard" className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300">
            <ArrowLeft className="w-4 h-4" />
          </Link>
          <div>
            <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
              <ShieldCheck className="w-6 h-6 text-cyan-400" />
              <span>Verified Proof Deep Inspection</span>
            </h1>
            <p className="text-xs text-slate-400 font-mono">Analysis ID: {analysis.id}</p>
          </div>
        </div>

        <button
          onClick={handleDownloadReport}
          className="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 font-semibold text-xs flex items-center gap-2 transition-colors"
        >
          <Download className="w-4 h-4 text-cyan-400" />
          <span>Download Proof Report (JSON)</span>
        </button>
      </div>

      <AnswerCard analysis={analysis} />

      {analysis.steps && <AnalysisTimeline steps={analysis.steps} />}

      {analysis.proof && <ProofCard proof={analysis.proof} />}

      {analysis.proof?.evidence_items && (
        <EvidencePanel items={analysis.proof.evidence_items} />
      )}
    </div>
  );
};
