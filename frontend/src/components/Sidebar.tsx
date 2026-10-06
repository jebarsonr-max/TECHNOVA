import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Database, Sparkles, History, Settings, FileSearch } from 'lucide-react';

export const Sidebar: React.FC = () => {
  const links = [
    { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { to: '/datasets', label: 'Datasets', icon: Database },
    { to: '/history', label: 'Analysis History', icon: History },
    { to: '/settings', label: 'System Health', icon: Settings },
  ];

  return (
    <aside className="w-64 glass-card border-r border-gray-800 hidden md:flex flex-col p-4 shrink-0 min-h-[calc(100vh-4rem)]">
      <div className="mb-6 px-2">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Navigation</span>
      </div>
      <nav className="space-y-1 flex-1">
        {links.map((link) => {
          const Icon = link.icon;
          return (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all ${
                  isActive
                    ? 'bg-gradient-to-r from-cyan-500/20 to-indigo-500/20 text-cyan-300 border border-cyan-500/30'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
                }`
              }
            >
              <Icon className="w-4 h-4" />
              <span>{link.label}</span>
            </NavLink>
          );
        })}
      </nav>

      <div className="p-3 rounded-xl bg-gradient-to-br from-cyan-950/40 to-indigo-950/40 border border-cyan-500/20 mt-auto">
        <div className="flex items-center gap-2 mb-2">
          <Sparkles className="w-4 h-4 text-cyan-400" />
          <span className="text-xs font-semibold text-cyan-300">Executable Proof</span>
        </div>
        <p className="text-xs text-slate-400 leading-relaxed">
          Every numerical answer is independently verified using DuckDB & sandboxed Python proof code.
        </p>
      </div>
    </aside>
  );
};
