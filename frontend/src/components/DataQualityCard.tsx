import React from 'react';
import { ShieldCheck, AlertTriangle, CheckCircle, Info } from 'lucide-react';
import { QualityReport } from '../types';

interface Props {
  report?: QualityReport;
}

export const DataQualityCard: React.FC<Props> = ({ report }) => {
  if (!report) return null;

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'EXCELLENT':
        return <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">EXCELLENT</span>;
      case 'GOOD':
        return <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">GOOD</span>;
      case 'NEEDS_ATTENTION':
        return <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/20">NEEDS ATTENTION</span>;
      default:
        return <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-rose-500/10 text-rose-400 border border-rose-500/20">POOR</span>;
    }
  };

  return (
    <div className="glass-card rounded-2xl p-6 border border-slate-800 space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500/20 to-teal-500/20 flex items-center justify-center border border-cyan-500/30">
            <ShieldCheck className="w-5 h-5 text-cyan-400" />
          </div>
          <div>
            <h3 className="font-semibold text-slate-100">Data Integrity & Quality Report</h3>
            <p className="text-xs text-slate-400">Automated structural health check</p>
          </div>
        </div>
        {getStatusBadge(report.status)}
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 pt-2">
        <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
          <span className="text-xs text-slate-500 block">Quality Score</span>
          <span className="text-xl font-bold text-slate-100 font-mono">{report.quality_score}%</span>
        </div>
        <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
          <span className="text-xs text-slate-500 block">Duplicate Rows</span>
          <span className="text-xl font-bold text-slate-100 font-mono">{report.duplicate_count}</span>
        </div>
        <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 col-span-2 sm:col-span-1">
          <span className="text-xs text-slate-500 block">Issues & Warnings</span>
          <span className="text-xl font-bold text-amber-400 font-mono">
            {report.issues.length + report.warnings.length}
          </span>
        </div>
      </div>

      {report.issues.length > 0 && (
        <div className="space-y-1.5 pt-2">
          <span className="text-xs font-semibold uppercase text-rose-400 tracking-wider">Critical Data Issues</span>
          {report.issues.map((iss, i) => (
            <div key={i} className="text-xs text-rose-300 bg-rose-500/10 p-2.5 rounded-xl border border-rose-500/20 flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 shrink-0 text-rose-400" />
              <span>{iss}</span>
            </div>
          ))}
        </div>
      )}

      {report.warnings.length > 0 && (
        <div className="space-y-1.5 pt-2">
          <span className="text-xs font-semibold uppercase text-amber-400 tracking-wider">Quality Warnings</span>
          {report.warnings.map((warn, i) => (
            <div key={i} className="text-xs text-amber-300 bg-amber-500/10 p-2.5 rounded-xl border border-amber-500/20 flex items-center gap-2">
              <Info className="w-4 h-4 shrink-0 text-amber-400" />
              <span>{warn}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
