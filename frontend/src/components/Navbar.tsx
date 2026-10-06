import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldCheck, Cpu, Database, History, Settings, Sparkles } from 'lucide-react';

export const Navbar: React.FC = () => {
  return (
    <header className="sticky top-0 z-50 glass-card border-b border-gray-800 bg-[#090d16]/90 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-3 group">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-cyan-500/20 group-hover:scale-105 transition-transform">
            <ShieldCheck className="w-6 h-6 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-xl tracking-tight text-white">TECHNOVA</span>
              <span className="px-2 py-0.5 text-[10px] font-semibold tracking-wide uppercase rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                Agentic GenAI
              </span>
            </div>
            <p className="text-xs text-slate-400 hidden sm:block">Proof-Carrying Data Analyst</p>
          </div>
        </Link>

        <nav className="flex items-center gap-1 sm:gap-2">
          <Link
            to="/dashboard"
            className="flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium text-slate-300 hover:text-white hover:bg-slate-800/60 transition-colors"
          >
            <Cpu className="w-4 h-4 text-cyan-400" />
            <span>Dashboard</span>
          </Link>

          <Link
            to="/datasets"
            className="flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium text-slate-300 hover:text-white hover:bg-slate-800/60 transition-colors"
          >
            <Database className="w-4 h-4 text-teal-400" />
            <span>Datasets</span>
          </Link>

          <Link
            to="/history"
            className="flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium text-slate-300 hover:text-white hover:bg-slate-800/60 transition-colors"
          >
            <History className="w-4 h-4 text-indigo-400" />
            <span>History</span>
          </Link>

          <Link
            to="/settings"
            className="flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium text-slate-300 hover:text-white hover:bg-slate-800/60 transition-colors"
          >
            <Settings className="w-4 h-4 text-slate-400" />
            <span className="hidden md:inline">Settings</span>
          </Link>
        </nav>
      </div>
    </header>
  );
};
