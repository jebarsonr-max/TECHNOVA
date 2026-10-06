import axios from 'axios';
import { Dataset, Analysis, Proof, EvidenceItem, Relationship, DemoQuestion } from '../types';

const API_BASE_URL = '/api';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  // Health
  getHealth: async () => {
    const res = await apiClient.get('/health');
    return res.data;
  },

  // Datasets
  uploadDataset: async (file: File): Promise<Dataset> => {
    const formData = new FormData();
    formData.append('file', file);
    const res = await apiClient.post<Dataset>('/datasets/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return res.data;
  },

  getDatasets: async (): Promise<Dataset[]> => {
    const res = await apiClient.get<Dataset[]>('/datasets');
    return res.data;
  },

  getDataset: async (id: string): Promise<Dataset> => {
    const res = await apiClient.get<Dataset>(`/datasets/${id}`);
    return res.data;
  },

  deleteDataset: async (id: string): Promise<void> => {
    await apiClient.delete(`/datasets/${id}`);
  },

  getRelationships: async (): Promise<Relationship[]> => {
    const res = await apiClient.get<Relationship[]>('/datasets/relationships');
    return res.data;
  },

  // Analysis
  createAnalysis: async (question: string, dataset_ids: string[]): Promise<Analysis> => {
    const res = await apiClient.post<Analysis>('/analysis', {
      question,
      dataset_ids,
    });
    return res.data;
  },

  getAnalysisHistory: async (): Promise<Analysis[]> => {
    const res = await apiClient.get<Analysis[]>('/analysis/history');
    return res.data;
  },

  getAnalysis: async (id: string): Promise<Analysis> => {
    const res = await apiClient.get<Analysis>(`/analysis/${id}`);
    return res.data;
  },

  // Proof & Evidence
  getProof: async (analysisId: string): Promise<Proof> => {
    const res = await apiClient.get<Proof>(`/analysis/${analysisId}/proof`);
    return res.data;
  },

  getEvidence: async (analysisId: string): Promise<EvidenceItem[]> => {
    const res = await apiClient.get<EvidenceItem[]>(`/analysis/${analysisId}/evidence`);
    return res.data;
  },

  // Reports
  getReport: async (analysisId: string): Promise<any> => {
    const res = await apiClient.get(`/reports/${analysisId}`);
    return res.data;
  },

  // Demo
  getDemoQuestions: async (): Promise<DemoQuestion[]> => {
    const res = await apiClient.get<DemoQuestion[]>('/demo/questions');
    return res.data;
  },
};
