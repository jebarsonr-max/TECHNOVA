import React from 'react';
import { CheckCircle2, AlertTriangle, AlertCircle, XCircle } from 'lucide-react';

interface Props {
  status: 'VERIFIED' | 'PARTIALLY_VERIFIED' | 'CANNOT_DETERMINE' | 'FAILED' | 'UNVERIFIED' | string;
  size?: 'sm' | 'md' | 'lg';
}

export const VerificationBadge: React.FC<Props> = ({ status, size = 'md' }) => {
  let badgeStyle = 'bg-slate-800 text-slate-300 border-slate-700';
  let icon = <AlertCircle className="w-4 h-4" />;
  let label = status;

  if (status === 'VERIFIED') {
    badgeStyle = 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30 shadow-emerald-500/10';
    icon = <CheckCircle2 className="w-4 h-4 text-emerald-400" />;
    label = 'VERIFIED PROOF';
  } else if (status === 'PARTIALLY_VERIFIED') {
    badgeStyle = 'bg-cyan-500/10 text-cyan-400 border-cyan-500/30';
    icon = <AlertTriangle className="w-4 h-4 text-cyan-400" />;
    label = 'PARTIALLY VERIFIED';
  } else if (status === 'CANNOT_DETERMINE') {
    badgeStyle = 'bg-amber-500/10 text-amber-400 border-amber-500/30';
    icon = <AlertTriangle className="w-4 h-4 text-amber-400" />;
    label = 'CANNOT DETERMINE (REFUSED)';
  } else if (status === 'FAILED') {
    badgeStyle = 'bg-rose-500/10 text-rose-400 border-rose-500/30';
    icon = <XCircle className="w-4 h-4 text-rose-400" />;
    label = 'VERIFICATION FAILED';
  }

  const sizeClasses = {
    sm: 'px-2 py-0.5 text-xs gap-1',
    md: 'px-3 py-1 text-xs gap-1.5 font-medium',
    lg: 'px-4 py-1.5 text-sm gap-2 font-semibold',
  }[size];

  return (
    <span
      className={`inline-flex items-center rounded-full border shadow-sm ${badgeStyle} ${sizeClasses}`}
    >
      {icon}
      <span>{label}</span>
    </span>
  );
};
