import React from 'react';
import { GitMerge, ArrowRight, AlertTriangle } from 'lucide-react';
import { Relationship } from '../types';

interface Props {
  relationships: Relationship[];
}

export const DataRelationshipGraph: React.FC<Props> = ({ relationships }) => {
  if (!relationships || relationships.length === 0) {
    return (
      <div className="p-4 rounded-xl bg-slate-900/40 border border-slate-800 text-xs text-slate-400 text-center">
        No multi-table relationships auto-detected yet. Upload 2+ datasets to see foreign-key join links.
      </div>
    );
  }

  return (
    <div className="glass-card rounded-2xl p-6 border border-slate-800 space-y-4">
      <div className="flex items-center gap-3 border-b border-slate-800 pb-3">
        <GitMerge className="w-5 h-5 text-cyan-400" />
        <h3 className="font-semibold text-slate-100">Auto-Detected Dataset Relationships</h3>
      </div>

      <div className="space-y-3">
        {relationships.map((rel, idx) => (
          <div key={idx} className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2 text-xs">
            <div className="flex flex-wrap items-center justify-between gap-2">
              <div className="flex items-center gap-2 font-mono text-cyan-300">
                <span className="bg-slate-800 px-2 py-1 rounded border border-slate-700">{rel.source_dataset_id.slice(0, 8)} ({rel.source_column})</span>
                <ArrowRight className="w-4 h-4 text-slate-500" />
                <span className="bg-slate-800 px-2 py-1 rounded border border-slate-700">{rel.target_dataset_id.slice(0, 8)} ({rel.target_column})</span>
              </div>
              <span className="px-2.5 py-0.5 rounded-full text-[10px] font-semibold uppercase bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                {rel.relationship_type}
              </span>
            </div>

            {rel.warnings && rel.warnings.length > 0 && (
              <div className="space-y-1 pt-1">
                {rel.warnings.map((w, wIdx) => (
                  <div key={wIdx} className="flex items-center gap-1.5 text-amber-400 text-[11px]">
                    <AlertTriangle className="w-3.5 h-3.5 shrink-0" />
                    <span>{w}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
