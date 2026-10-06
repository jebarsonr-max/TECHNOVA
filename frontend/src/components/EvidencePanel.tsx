import React from 'react';
import { FileCheck, Database, Layers, CheckCircle2 } from 'lucide-react';
import { EvidenceItem } from '../types';

interface Props {
  items: EvidenceItem[];
}

export const EvidencePanel: React.FC<Props> = ({ items }) => {
  if (!items || items.length === 0) return null;

  return (
    <div className="glass-card rounded-2xl p-6 border border-slate-800 space-y-4">
      <div className="flex items-center gap-3 border-b border-slate-800 pb-3">
        <FileCheck className="w-5 h-5 text-cyan-400" />
        <h3 className="font-semibold text-slate-100">Verification Evidence Bundle</h3>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {items.map((ev) => (
          <div key={ev.id} className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
              <h4 className="text-xs font-semibold text-slate-200">{ev.title}</h4>
            </div>
            <pre className="text-[11px] font-mono text-cyan-300/80 bg-slate-950 p-2.5 rounded-lg overflow-x-auto">
              {JSON.stringify(ev.content, null, 2)}
            </pre>
          </div>
        ))}
      </div>
    </div>
  );
};
