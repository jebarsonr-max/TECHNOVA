import React from 'react';
import { ShieldCheck, Cpu, Terminal, FileCode, CheckCircle, Database, Filter } from 'lucide-react';
import { Proof } from '../types';
import { VerificationBadge } from './VerificationBadge';
import { ConfidenceIndicator } from './ConfidenceIndicator';
import { CodeViewer } from './CodeViewer';

interface Props {
  proof: Proof;
}

export const ProofCard: React.FC<Props> = ({ proof }) => {
  return (
    <div className="glass-card rounded-2xl p-6 border border-slate-800 space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500/20 to-indigo-500/20 flex items-center justify-center border border-cyan-500/30">
            <ShieldCheck className="w-5 h-5 text-cyan-400" />
          </div>
          <div>
            <h3 className="font-semibold text-slate-100 text-lg">Executable Proof Card</h3>
            <p className="text-xs text-slate-400">Deterministic code, sandbox execution, and independent verification</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <VerificationBadge status={proof.verification_status} size="md" />
          <div className="w-32 hidden sm:block">
            <ConfidenceIndicator score={proof.verification_score} />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
        <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1">
          <span className="text-slate-500 flex items-center gap-1.5 font-medium">
            <Database className="w-3.5 h-3.5 text-cyan-400" /> Source Datasets
          </span>
          <p className="font-semibold text-slate-200 truncate">
            {proof.source_datasets?.join(', ') || 'Immutable dataset'}
          </p>
        </div>

        <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1">
          <span className="text-slate-500 flex items-center gap-1.5 font-medium">
            <Filter className="w-3.5 h-3.5 text-indigo-400" /> Relevant Columns
          </span>
          <p className="font-semibold text-slate-200 truncate">
            {proof.relevant_columns?.join(', ') || 'All numeric'}
          </p>
        </div>

        <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1">
          <span className="text-slate-500 flex items-center gap-1.5 font-medium">
            <Terminal className="w-3.5 h-3.5 text-emerald-400" /> Execution Status
          </span>
          <p className="font-semibold text-emerald-400 font-mono">
            {proof.execution_status} ({proof.execution_result?.execution_time_ms ?? 0} ms)
          </p>
        </div>
      </div>

      {proof.calculation_explanation && (
        <div className="p-4 rounded-xl bg-slate-900/40 border border-slate-800 space-y-1">
          <span className="text-xs font-semibold uppercase text-slate-400 tracking-wider">Calculation Method</span>
          <p className="text-xs text-slate-300 leading-relaxed">{proof.calculation_explanation}</p>
        </div>
      )}

      <div className="space-y-2">
        <span className="text-xs font-semibold uppercase text-slate-400 tracking-wider flex items-center gap-1.5">
          <FileCode className="w-4 h-4 text-cyan-400" /> Generated Analytical Proof Code
        </span>
        <CodeViewer code={proof.generated_code} language={proof.code_language} />
      </div>

      {proof.verification_result && (
        <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-3 text-xs">
          <span className="font-semibold text-slate-200 block">Verification Engine Breakdown</span>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
            <div className="flex items-center gap-2 p-2 rounded-lg bg-slate-800/60">
              <CheckCircle className={`w-3.5 h-3.5 ${proof.verification_result.reproducibility_passed ? 'text-emerald-400' : 'text-rose-400'}`} />
              <span>Reproducibility</span>
            </div>
            <div className="flex items-center gap-2 p-2 rounded-lg bg-slate-800/60">
              <CheckCircle className={`w-3.5 h-3.5 ${proof.verification_result.math_check_passed ? 'text-emerald-400' : 'text-rose-400'}`} />
              <span>DuckDB Check</span>
            </div>
            <div className="flex items-center gap-2 p-2 rounded-lg bg-slate-800/60">
              <CheckCircle className={`w-3.5 h-3.5 ${proof.verification_result.unit_check_passed ? 'text-emerald-400' : 'text-rose-400'}`} />
              <span>Unit Compatibility</span>
            </div>
            <div className="flex items-center gap-2 p-2 rounded-lg bg-slate-800/60">
              <CheckCircle className={`w-3.5 h-3.5 ${proof.verification_result.data_quality_check_passed ? 'text-emerald-400' : 'text-rose-400'}`} />
              <span>Data Quality</span>
            </div>
          </div>
          {proof.verification_result.verification_notes && (
            <p className="text-slate-400 italic text-[11px] pt-1">
              Note: {proof.verification_result.verification_notes}
            </p>
          )}
        </div>
      )}
    </div>
  );
};
