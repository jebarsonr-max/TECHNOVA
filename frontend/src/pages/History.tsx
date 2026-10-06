import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { History, ShieldCheck, ArrowRight } from 'lucide-react';
import { apiService } from '../services/api';
import { Analysis } from '../types';
import { VerificationBadge } from '../components/VerificationBadge';
import { LoadingState, EmptyState } from '../components/States';

export const HistoryPage: React.FC = () => {
  const [history, setHistory] = useState<Analysis[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiService
      .getAnalysisHistory()
      .then(setHistory)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <LoadingState label="Loading analysis trajectory log..." />;
  if (history.length === 0) return <EmptyState title="No Past Analyses" description="Ask a question on a dataset to generate proof history." />;

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
          <History className="w-6 h-6 text-indigo-400" />
          <span>Analysis History & Audit Trail</span>
        </h1>
        <p className="text-xs text-slate-400">Complete log of all executed analysis questions and verification statuses</p>
      </div>

      <div className="space-y-3">
        {history.map((item) => (
          <Link
            key={item.id}
            to={`/proof/${item.id}`}
            className="block p-5 rounded-2xl glass-card glass-card-hover border border-slate-800 space-y-3"
          >
            <div className="flex flex-wrap items-center justify-between gap-3">
              <h3 className="font-semibold text-slate-100 text-sm">{item.question}</h3>
              <VerificationBadge status={item.verification_status} size="sm" />
            </div>

            <div className="flex items-center justify-between text-xs text-slate-400 pt-2 border-t border-slate-800">
              <span>{new Date(item.created_at).toLocaleString()}</span>
              <div className="flex items-center gap-2">
                <span className="font-mono text-cyan-300 font-semibold">{item.final_answer}</span>
                <ArrowRight className="w-4 h-4 text-slate-500" />
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
};
