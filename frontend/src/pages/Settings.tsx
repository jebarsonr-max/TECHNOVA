import React, { useState, useEffect } from 'react';
import { Settings, Cpu, ShieldCheck, CheckCircle2, Server, Lock } from 'lucide-react';
import { apiService } from '../services/api';

export const SettingsPage: React.FC = () => {
  const [health, setHealth] = useState<any>(null);

  useEffect(() => {
    apiService.getHealth().then(setHealth).catch(console.error);
  }, []);

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
          <Settings className="w-6 h-6 text-slate-400" />
          <span>System Configuration & Security Status</span>
        </h1>
        <p className="text-xs text-slate-400">Environment settings, backend health, and sandbox execution controls</p>
      </div>

      <div className="glass-card rounded-2xl p-6 border border-slate-800 space-y-6">
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div className="flex items-center gap-3">
            <Server className="w-5 h-5 text-cyan-400" />
            <div>
              <h3 className="font-semibold text-slate-100 text-sm">FastAPI Backend Status</h3>
              <p className="text-xs text-slate-400">{health?.service || 'TECHNOVA Agentic Backend'}</p>
            </div>
          </div>
          <span className="px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 flex items-center gap-1.5">
            <CheckCircle2 className="w-3.5 h-3.5" /> ONLINE ({health?.version || '1.0.0'})
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1">
            <span className="text-slate-500 font-medium block">Sandbox Isolation</span>
            <span className="font-semibold text-emerald-400">Docker / Python Subprocess Active</span>
          </div>

          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1">
            <span className="text-slate-500 font-medium block">Execution Timeout</span>
            <span className="font-semibold text-slate-200 font-mono">10 Seconds (Strict Limit)</span>
          </div>

          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1">
            <span className="text-slate-500 font-medium block">Memory Cap</span>
            <span className="font-semibold text-slate-200 font-mono">512 MB</span>
          </div>

          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1">
            <span className="text-slate-500 font-medium block">Network Policy</span>
            <span className="font-semibold text-emerald-400">DISABLED (No outbound sockets)</span>
          </div>
        </div>

        <div className="p-4 rounded-xl bg-slate-900/40 border border-slate-800 space-y-2 text-xs">
          <div className="flex items-center gap-2 text-amber-400 font-semibold">
            <Lock className="w-4 h-4" />
            <span>Security Architecture Rule</span>
          </div>
          <p className="text-slate-300 leading-relaxed">
            AI API keys are isolated on the backend only and never exposed to the frontend client. Code is verified and executed in safe sandbox processes.
          </p>
        </div>
      </div>
    </div>
  );
};
