import React, { useState, useEffect } from 'react';
import { Database, Plus } from 'lucide-react';
import { apiService } from '../services/api';
import { Dataset, Relationship } from '../types';
import { DatasetCard } from '../components/DatasetCard';
import { UploadZone } from '../components/UploadZone';
import { DataRelationshipGraph } from '../components/DataRelationshipGraph';
import { LoadingState } from '../components/States';

export const DatasetsPage: React.FC = () => {
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [relationships, setRelationships] = useState<Relationship[]>([]);
  const [loading, setLoading] = useState(true);
  const [showUpload, setShowUpload] = useState(false);

  useEffect(() => {
    fetchDatasetsData();
  }, []);

  const fetchDatasetsData = async () => {
    setLoading(true);
    try {
      const [dsList, rels] = await Promise.all([
        apiService.getDatasets(),
        apiService.getRelationships(),
      ]);
      setDatasets(dsList);
      setRelationships(rels);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this dataset?')) return;
    try {
      await apiService.deleteDataset(id);
      setDatasets((prev) => prev.filter((d) => d.id !== id));
    } catch (err) {
      alert('Failed to delete dataset.');
    }
  };

  if (loading) return <LoadingState label="Loading datasets & schema graph..." />;

  return (
    <div className="space-y-8">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <Database className="w-6 h-6 text-teal-400" />
            <span>Dataset Repository</span>
          </h1>
          <p className="text-xs text-slate-400">Immutable data sources for proof-carrying analysis</p>
        </div>

        <button
          onClick={() => setShowUpload(!showUpload)}
          className="px-4 py-2.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-semibold text-xs flex items-center gap-2 transition-colors shadow-lg shadow-cyan-500/20"
        >
          <Plus className="w-4 h-4" />
          <span>Upload Dataset</span>
        </button>
      </div>

      {showUpload && <UploadZone onDatasetUploaded={(ds) => { setDatasets([ds, ...datasets]); setShowUpload(false); }} />}

      <DataRelationshipGraph relationships={relationships} />

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {datasets.map((ds) => (
          <DatasetCard key={ds.id} dataset={ds} onDelete={handleDelete} />
        ))}
      </div>
    </div>
  );
};
