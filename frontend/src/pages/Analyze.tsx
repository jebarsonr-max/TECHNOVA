import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Sparkles, Send, Cpu, Database, ArrowRight, ShieldCheck, Loader2 } from 'lucide-react';
import { apiService } from '../services/api';
import { Dataset } from '../types';
import { LoadingState } from '../components/States';

export const AnalyzePage: React.FC = () => {
  const { datasetId } = useParams<{ datasetId: string }>();
  const [dataset, setDataset] = useState<Dataset | null>(null);
  const [allDatasets, setAllDatasets] = useState<Dataset[]>([]);
  const [selectedDatasetIds, setSelectedDatasetIds] = useState<string[]>([]);
  const [question, setQuestion] = useState('');
  const [analyzing, setAnalyzing] = useState(false);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadData();
  }, [datasetId]);

  const loadData = async () => {
    setLoading(true);
    try {
      const list = await apiService.getDatasets();
      setAllDatasets(list);
      if (datasetId) {
        setSelectedDatasetIds([datasetId]);
        const target = list.find((d) => d.id === datasetId);
        if (target) setDataset(target);
      } else if (list.length > 0) {
        setSelectedDatasetIds([list[0].id]);
        setDataset(list[0]);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAskQuestion = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim() || selectedDatasetIds.length === 0) return;

    setAnalyzing(true);
    try {
      const analysis = await apiService.createAnalysis(question, selectedDatasetIds);
      navigate(`/proof/${analysis.id}`);
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Analysis pipeline execution failed.');
    } finally {
      setAnalyzing(false);
    }
  };

  if (loading) return <LoadingState label="Loading data studio..." />;

  return (
    <div className="max-w-4xl mx-auto space-y-8 py-4">
      <div className="text-center space-y-2">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 text-xs font-semibold">
          <Sparkles className="w-4 h-4" />
          <span>Proof-Carrying AI Analyst</span>
        </div>
        <h1 className="text-3xl font-bold text-slate-100">Ask Natural Language Questions</h1>
        <p className="text-xs text-slate-400">
          Selected dataset(s) will be inspected for schemas, traps, and mathematical proofs.
        </p>
      </div>

      {/* Dataset Selector */}
      <div className="glass-card rounded-2xl p-5 border border-slate-800 space-y-3">
        <span className="text-xs font-semibold uppercase text-slate-400 tracking-wider flex items-center gap-1.5">
          <Database className="w-4 h-4 text-cyan-400" /> Target Datasets
        </span>
        <div className="flex flex-wrap gap-2">
          {allDatasets.map((ds) => {
            const isSelected = selectedDatasetIds.includes(ds.id);
            return (
              <button
                key={ds.id}
                type="button"
                onClick={() => {
                  if (isSelected) {
                    if (selectedDatasetIds.length > 1) {
                      setSelectedDatasetIds(selectedDatasetIds.filter((i) => i !== ds.id));
                    }
                  } else {
                    setSelectedDatasetIds([...selectedDatasetIds, ds.id]);
                  }
                }}
                className={`px-3 py-2 rounded-xl text-xs font-medium transition-all ${
                  isSelected
                    ? 'bg-gradient-to-r from-cyan-500 to-indigo-600 text-white shadow-md'
                    : 'bg-slate-900 text-slate-400 border border-slate-800 hover:border-slate-700'
                }`}
              >
                {ds.original_filename} ({ds.row_count} rows)
              </button>
            );
          })}
        </div>
      </div>

      {/* Question Form */}
      <form onSubmit={handleAskQuestion} className="glass-card rounded-2xl p-6 border border-cyan-500/30 space-y-4 shadow-2xl">
        <div className="space-y-2">
          <label className="text-xs font-semibold uppercase text-slate-400 tracking-wider">
            Your Analytical Question
          </label>
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="e.g. What is the total order amount across all completed transactions?"
            rows={4}
            required
            className="w-full rounded-xl bg-slate-900 border border-slate-800 p-4 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-400 transition-colors font-sans"
          />
        </div>

        <button
          type="submit"
          disabled={analyzing || !question.trim()}
          className="w-full py-4 rounded-xl bg-gradient-to-r from-cyan-500 via-teal-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-white font-bold text-sm shadow-xl shadow-cyan-500/20 transition-all flex items-center justify-center gap-2 disabled:opacity-50"
        >
          {analyzing ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              <span>Running Proof-Carrying State Machine...</span>
            </>
          ) : (
            <>
              <ShieldCheck className="w-5 h-5" />
              <span>Generate Answer with Executable Proof</span>
            </>
          )}
        </button>
      </form>
    </div>
  );
};
