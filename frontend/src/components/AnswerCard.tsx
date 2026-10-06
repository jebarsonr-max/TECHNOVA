import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldCheck, Cpu, ArrowRight, AlertTriangle, CheckCircle2 } from 'lucide-react';
import { VerificationBadge } from './VerificationBadge';
import { ConfidenceIndicator } from './ConfidenceIndicator';
import { Analysis } from '../types';

interface Props {
  analysis: Analysis;
}

export const AnswerCard: React.FC<Props> = ({ analysis }) => {
  const isRefusal = analysis.verification_status === 'CANNOT_DETERMINE' || analysis.status === 'CANNOT_DETERMINE';

  return (
    <div className={`glass-card rounded-2xl p-6 border ${isRefusal ? 'border-amber-500/30 bg-amber-950/10' : 'border-cyan-500/30 bg-cyan-950/10'} space-y-6 shadow-xl`}>
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className={`w-12 h-12 rounded-2xl ${isRefusal ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' : 'bg-gradient-to-tr from-cyan-500 to-indigo-600 text-white shadow-lg shadow-cyan-500/20'} flex items-center justify-center font-bold`}>
            {isRefusal ? <AlertTriangle className="w-6 h-6" /> : <ShieldCheck className="w-6 h-6" />}
          </div>
          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-400">
              {isRefusal ? 'System Refusal (No Guessing Rule)' : 'Verified Numerical Answer'}
            </h3>
            <p className="text-xs text-slate-400">{analysis.question}</p>
          </div>
        </div>

        <VerificationBadge status={analysis.verification_status} size="lg" />
      </div>

      <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-3">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">Result Output</span>
        {isRefusal ? (
          <div className="space-y-2">
            <div className="text-xl font-bold text-amber-400 font-mono">
              CANNOT_DETERMINE
            </div>
            <p className="text-sm text-slate-300 leading-relaxed bg-amber-500/10 p-4 rounded-xl border border-amber-500/20">
              {analysis.refusal_reason || analysis.final_answer}
            </p>
          </div>
        ) : (
          <div className="space-y-1">
            <div className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-cyan-300 via-emerald-300 to-white font-mono tracking-tight">
              {analysis.final_answer}
            </div>
            <p className="text-xs text-slate-400 pt-1">
              Calculated via sandboxed Python execution & DuckDB cross-check.
            </p>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div className="p-4 rounded-xl bg-slate-900/50 border border-slate-800 space-y-1">
          <span className="text-xs text-slate-400 block">Verification Confidence</span>
          <ConfidenceIndicator score={analysis.verification_score} />
        </div>
        <div className="p-4 rounded-xl bg-slate-900/50 border border-slate-800 flex items-center justify-between">
          <div>
            <span className="text-xs text-slate-400 block">Executable Proof</span>
            <span className="text-xs font-semibold text-emerald-400 flex items-center gap-1">
              <CheckCircle2 className="w-3.5 h-3.5" /> Code Executed & Verified
            </span>
          </div>
          {analysis.proof && (
            <Link
              to={`/proof/${analysis.id}`}
              className="px-3 py-2 rounded-xl bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 text-xs font-semibold flex items-center gap-1.5 transition-colors"
            >
              <span>Inspect Proof</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          )}
        </div>
      </div>
    </div>
  );
};
