import React from 'react';
import { Link } from 'react-router-dom';
import { FileSpreadsheet, Table, ShieldCheck, ArrowRight, Trash2 } from 'lucide-react';
import { Dataset } from '../types';

interface Props {
  dataset: Dataset;
  onDelete?: (id: string) => void;
}

export const DatasetCard: React.FC<Props> = ({ dataset, onDelete }) => {
  const qualityScore = dataset.quality_report?.quality_score ?? 100;

  return (
    <div className="glass-card glass-card-hover rounded-2xl p-5 flex flex-col justify-between">
      <div>
        <div className="flex items-start justify-between gap-3 mb-3">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400">
              <FileSpreadsheet className="w-5 h-5" />
            </div>
            <div>
              <h4 className="font-semibold text-slate-100 truncate max-w-[180px]" title={dataset.original_filename}>
                {dataset.original_filename}
              </h4>
              <span className="text-xs text-slate-400 uppercase tracking-wider">{dataset.file_type}</span>
            </div>
          </div>

          {onDelete && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                onDelete(dataset.id);
              }}
              className="text-slate-500 hover:text-rose-400 p-1.5 rounded-lg hover:bg-slate-800 transition-colors"
              title="Delete dataset"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          )}
        </div>

        <div className="grid grid-cols-2 gap-2 my-4 p-3 rounded-xl bg-slate-900/60 border border-slate-800 text-xs">
          <div>
            <span className="text-slate-500 block">Rows</span>
            <span className="font-semibold text-slate-200 font-mono">{dataset.row_count.toLocaleString()}</span>
          </div>
          <div>
            <span className="text-slate-500 block">Columns</span>
            <span className="font-semibold text-slate-200 font-mono">{dataset.column_count}</span>
          </div>
        </div>

        <div className="flex items-center justify-between text-xs mb-4">
          <span className="text-slate-400">Quality Score</span>
          <span className={`font-semibold ${qualityScore >= 80 ? 'text-emerald-400' : 'text-amber-400'}`}>
            {qualityScore}%
          </span>
        </div>
      </div>

      <div className="flex items-center gap-2 pt-3 border-t border-slate-800">
        <Link
          to={`/datasets/${dataset.id}`}
          className="flex-1 py-2 px-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-medium text-slate-200 text-center transition-colors flex items-center justify-center gap-1.5"
        >
          <Table className="w-3.5 h-3.5 text-cyan-400" />
          <span>Profile</span>
        </Link>
        <Link
          to={`/analyze/${dataset.id}`}
          className="flex-1 py-2 px-3 rounded-xl bg-gradient-to-r from-cyan-600 to-indigo-600 hover:from-cyan-500 hover:to-indigo-500 text-xs font-semibold text-white text-center transition-colors flex items-center justify-center gap-1.5 shadow-md shadow-cyan-600/20"
        >
          <span>Ask AI</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </Link>
      </div>
    </div>
  );
};
