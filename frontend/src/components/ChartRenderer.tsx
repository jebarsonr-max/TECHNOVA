import React from 'react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

interface Props {
  data: any[];
  xKey?: string;
  yKey?: string;
  title?: string;
}

export const ChartRenderer: React.FC<Props> = ({
  data,
  xKey = 'name',
  yKey = 'value',
  title = 'Verified Data Visualization',
}) => {
  if (!data || data.length === 0) return null;

  return (
    <div className="glass-card rounded-2xl p-6 border border-slate-800 space-y-4">
      <h4 className="text-sm font-semibold text-slate-200">{title}</h4>
      <div className="h-64 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
            <XAxis dataKey={xKey} stroke="#9ca3af" fontSize={12} />
            <YAxis stroke="#9ca3af" fontSize={12} />
            <Tooltip
              contentStyle={{ backgroundColor: '#111827', borderColor: '#374151', color: '#f3f4f6', borderRadius: '0.75rem' }}
            />
            <Bar dataKey={yKey} fill="#06b6d4" radius={[6, 6, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
