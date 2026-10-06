import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldCheck, Cpu, Database, CheckCircle2, ArrowRight, Lock, Code2, AlertTriangle, FileCode } from 'lucide-react';

export const LandingPage: React.FC = () => {
  return (
    <div className="space-y-16 py-8 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
      {/* Hero Section */}
      <section className="text-center space-y-6 pt-12">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 text-cyan-300 border border-cyan-500/20 text-xs font-semibold">
          <ShieldCheck className="w-4 h-4 text-cyan-400" />
          <span>PSI PS08: Proof-Carrying Data Analyst</span>
        </div>

        <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-white max-w-4xl mx-auto leading-tight">
          An AI data analyst that does not just give an answer.{' '}
          <span className="gradient-text">It gives executable proof behind the answer.</span>
        </h1>

        <p className="text-slate-400 text-base sm:text-lg max-w-2xl mx-auto leading-relaxed">
          Upload messy real-world datasets, ask natural language questions, and receive mathematically verified answers backed by sandboxed Python code and DuckDB cross-checks.
        </p>

        <div className="flex flex-wrap items-center justify-center gap-4 pt-4">
          <Link
            to="/dashboard"
            className="px-6 py-3.5 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-white font-semibold text-sm shadow-xl shadow-cyan-500/20 transition-all flex items-center gap-2 scale-105"
          >
            <span>Launch Analytics Studio</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
          <Link
            to="/datasets"
            className="px-6 py-3.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold text-sm border border-slate-700 transition-colors flex items-center gap-2"
          >
            <Database className="w-4 h-4 text-cyan-400" />
            <span>Explore Demo Datasets</span>
          </Link>
        </div>
      </section>

      {/* Core Features Grid */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass-card rounded-2xl p-6 border border-slate-800 space-y-3">
          <div className="w-12 h-12 rounded-xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 flex items-center justify-center">
            <Lock className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-semibold text-slate-100">Strict No-Guess Rule</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            If data is missing, ambiguous, or contradictory, TECHNOVA returns <code className="text-amber-400 font-mono">CANNOT_DETERMINE</code> instead of fabricating hallucinated answers.
          </p>
        </div>

        <div className="glass-card rounded-2xl p-6 border border-slate-800 space-y-3">
          <div className="w-12 h-12 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 flex items-center justify-center">
            <Code2 className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-semibold text-slate-100">Sandboxed Execution</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            All AI-generated analytical code runs inside network-disabled, timeout-controlled execution sandboxes. Host machines are completely protected.
          </p>
        </div>

        <div className="glass-card rounded-2xl p-6 border border-slate-800 space-y-3">
          <div className="w-12 h-12 rounded-xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 flex items-center justify-center">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-semibold text-slate-100">DuckDB Independent Cross-Check</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Primary pandas calculations are cross-verified against DuckDB SQL query execution to ensure 100% mathematical reproducibility.
          </p>
        </div>
      </section>

      {/* Adversarial Trap Handling Section */}
      <section className="glass-card rounded-3xl p-8 border border-slate-800 space-y-6">
        <div className="flex items-center gap-3">
          <AlertTriangle className="w-6 h-6 text-amber-400" />
          <div>
            <h2 className="text-xl font-bold text-slate-100">PS08 Adversarial Trap Detection</h2>
            <p className="text-xs text-slate-400">Guaranteed refusal handling for trick questions and incomplete datasets</p>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 text-xs">
          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1">
            <span className="font-semibold text-amber-400 block">Unit / Currency Mismatch</span>
            <p className="text-slate-400">Refuses profit calculations when revenue is in USD and costs in EUR without exchange rates.</p>
          </div>

          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1">
            <span className="font-semibold text-amber-400 block">Missing Cost Data</span>
            <p className="text-slate-400">Refuses profit margin questions when cost columns are absent in source datasets.</p>
          </div>

          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1">
            <span className="font-semibold text-amber-400 block">Future Prediction Trap</span>
            <p className="text-slate-400">Refuses next-year revenue forecasts when dataset only contains historical transactions.</p>
          </div>
        </div>
      </section>
    </div>
  );
};
