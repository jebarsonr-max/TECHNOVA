import React from 'react';

interface Props {
  score: number; // 0.0 to 1.0
}

export const ConfidenceIndicator: React.FC<Props> = ({ score }) => {
  const percentage = Math.round(score * 100);
  let color = 'bg-emerald-500';
  if (score < 0.6) color = 'bg-rose-500';
  else if (score < 0.85) color = 'bg-cyan-500';

  return (
    <div className="flex items-center gap-3">
      <div className="flex-1 bg-slate-800 h-2 rounded-full overflow-hidden border border-slate-700">
        <div
          className={`h-full ${color} transition-all duration-500 rounded-full`}
          style={{ width: `${percentage}%` }}
        />
      </div>
      <span className="text-xs font-semibold text-slate-300 font-mono">{percentage}%</span>
    </div>
  );
};
