import React from 'react';
import { AlertCircle, Loader2, Database, Inbox } from 'lucide-react';

export const ErrorState: React.FC<{ message: string }> = ({ message }) => (
  <div className="p-8 rounded-2xl glass-card border border-rose-500/20 text-center space-y-3">
    <div className="w-12 h-12 rounded-full bg-rose-500/10 text-rose-400 flex items-center justify-center mx-auto">
      <AlertCircle className="w-6 h-6" />
    </div>
    <h4 className="text-base font-semibold text-rose-300">An Error Occurred</h4>
    <p className="text-xs text-slate-400 max-w-md mx-auto">{message}</p>
  </div>
);

export const LoadingState: React.FC<{ label?: string }> = ({ label = 'Processing...' }) => (
  <div className="p-12 text-center space-y-3">
    <Loader2 className="w-8 h-8 text-cyan-400 animate-spin mx-auto" />
    <p className="text-xs text-slate-400 font-medium">{label}</p>
  </div>
);

export const EmptyState: React.FC<{ title?: string; description?: string }> = ({
  title = 'No Data Found',
  description = 'Upload a dataset to get started with proof-carrying analytics.',
}) => (
  <div className="p-12 glass-card rounded-2xl border border-slate-800 text-center space-y-3">
    <div className="w-12 h-12 rounded-full bg-slate-800 text-slate-400 flex items-center justify-center mx-auto">
      <Inbox className="w-6 h-6" />
    </div>
    <h4 className="text-base font-semibold text-slate-200">{title}</h4>
    <p className="text-xs text-slate-400 max-w-sm mx-auto">{description}</p>
  </div>
);
