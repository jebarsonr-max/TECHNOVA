import React from 'react';

interface Props {
  columns: string[];
  data: any[];
}

export const DataTable: React.FC<Props> = ({ columns, data }) => {
  if (!data || data.length === 0) return null;

  return (
    <div className="overflow-x-auto rounded-2xl border border-slate-800 bg-slate-900/60">
      <table className="w-full text-left text-xs text-slate-300">
        <thead className="bg-slate-950 text-slate-400 uppercase tracking-wider font-semibold border-b border-slate-800">
          <tr>
            {columns.map((col, idx) => (
              <th key={idx} className="px-4 py-3">
                {col}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-800">
          {data.map((row, rIdx) => (
            <tr key={rIdx} className="hover:bg-slate-800/40 transition-colors">
              {columns.map((col, cIdx) => (
                <td key={cIdx} className="px-4 py-3 font-mono">
                  {String(row[col] ?? '')}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
