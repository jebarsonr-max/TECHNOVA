import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Table, FileSpreadsheet, ArrowLeft, ShieldCheck, CheckCircle2 } from 'lucide-react';
import { apiService } from '../services/api';
import { Dataset } from '../types';
import { DataQualityCard } from '../components/DataQualityCard';
import { LoadingState, ErrorState } from '../components/States';

export const DatasetDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [dataset, setDataset] = useState<Dataset | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (id) {
      apiService
        .getDataset(id)
        .then(setDataset)
        .catch((err) => setError(err.message))
        .finally(() => setLoading(false));
    }
  }, [id]);

  if (loading) return <LoadingState label="Inspecting dataset schema..." />;
  if (error || !dataset) return <ErrorState message={error || 'Dataset not found'} />;

  return (
    <div className="space-y-8">
      <div className="flex items-center gap-3">
        <Link to="/datasets" className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300">
          <ArrowLeft className="w-4 h-4" />
        </Link>
        <div>
          <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <FileSpreadsheet className="w-6 h-6 text-cyan-400" />
            <span>{dataset.original_filename}</span>
          </h1>
          <p className="text-xs text-slate-400 font-mono">ID: {dataset.id}</p>
        </div>
      </div>

      <DataQualityCard report={dataset.quality_report} />

      <div className="glass-card rounded-2xl p-6 border border-slate-800 space-y-4">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <h3 className="font-semibold text-slate-100 flex items-center gap-2">
            <Table className="w-5 h-5 text-indigo-400" />
            <span>Schema & Column Profiling</span>
          </h3>
          <span className="text-xs text-slate-400 font-mono">{dataset.columns.length} columns profiled</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-950 text-slate-400 uppercase tracking-wider font-semibold border-b border-slate-800">
              <tr>
                <th className="px-4 py-3">Column Name</th>
                <th className="px-4 py-3">Detected Type</th>
                <th className="px-4 py-3">Missing</th>
                <th className="px-4 py-3">Unique</th>
                <th className="px-4 py-3">Min / Max</th>
                <th className="px-4 py-3">Unit / Currency</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {dataset.columns.map((col) => (
                <tr key={col.id} className="hover:bg-slate-800/40 transition-colors">
                  <td className="px-4 py-3 font-semibold text-cyan-300 flex items-center gap-2">
                    <span>{col.name}</span>
                    {col.is_identifier && (
                      <span className="px-1.5 py-0.5 rounded text-[10px] bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">ID</span>
                    )}
                  </td>
                  <td className="px-4 py-3 font-mono text-slate-400">{col.detected_type}</td>
                  <td className="px-4 py-3 font-mono">{col.missing_count}</td>
                  <td className="px-4 py-3 font-mono">{col.unique_count}</td>
                  <td className="px-4 py-3 font-mono text-slate-400">
                    {col.min_value ? `${col.min_value} / ${col.max_value}` : '-'}
                  </td>
                  <td className="px-4 py-3 font-mono text-emerald-400">
                    {col.currency_symbol || col.detected_unit || '-'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
