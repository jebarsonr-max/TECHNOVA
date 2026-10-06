import React from 'react';
import { CheckCircle2, Clock, AlertTriangle, Loader2 } from 'lucide-react';
import { AnalysisStep } from '../types';

interface Props {
  steps: AnalysisStep[];
}

export const AnalysisTimeline: React.FC<Props> = ({ steps }) => {
  if (!steps || steps.length === 0) return null;

  return (
    <div className="space-y-4">
      <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400">Agentic Execution Timeline</h4>
      <div className="relative border-l-2 border-slate-800 ml-3 space-y-6">
        {steps.map((step) => {
          let stepIcon = <CheckCircle2 className="w-5 h-5 text-emerald-400" />;
          let circleBg = 'bg-emerald-500/10 border-emerald-500/40';

          if (step.status === 'IN_PROGRESS') {
            stepIcon = <Loader2 className="w-5 h-5 text-cyan-400 animate-spin" />;
            circleBg = 'bg-cyan-500/10 border-cyan-500/40';
          } else if (step.status === 'FAILED') {
            stepIcon = <AlertTriangle className="w-5 h-5 text-rose-400" />;
            circleBg = 'bg-rose-500/10 border-rose-500/40';
          }

          return (
            <div key={step.id} className="relative pl-6">
              <div className={`absolute -left-[15px] top-0.5 w-7 h-7 rounded-full border flex items-center justify-center ${circleBg} bg-[#090d16]`}>
                {stepIcon}
              </div>
              <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1">
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-xs text-slate-200">{step.title}</span>
                  <span className="text-[10px] text-slate-500 uppercase">{step.status}</span>
                </div>
                {step.description && (
                  <p className="text-xs text-slate-400 leading-relaxed">{step.description}</p>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
