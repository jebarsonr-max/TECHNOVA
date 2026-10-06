export interface DatasetColumn {
  id: string;
  name: string;
  data_type: string;
  detected_type: string;
  missing_count: number;
  unique_count: number;
  min_value?: string;
  max_value?: string;
  mean_value?: number;
  currency_symbol?: string;
  detected_unit?: string;
  is_identifier: boolean;
  suspicious_values?: any[];
}

export interface QualityReport {
  quality_score: number;
  status: 'EXCELLENT' | 'GOOD' | 'NEEDS_ATTENTION' | 'POOR';
  duplicate_count: number;
  issues: string[];
  warnings: string[];
}

export interface Dataset {
  id: string;
  filename: string;
  original_filename: string;
  file_type: string;
  file_size_bytes: number;
  row_count: number;
  column_count: number;
  created_at: string;
  columns: DatasetColumn[];
  profiling_summary?: any;
  quality_report?: QualityReport;
}

export interface ExecutionResult {
  id: string;
  exit_code: number;
  stdout?: string;
  stderr?: string;
  execution_time_ms: number;
  result_data?: any;
  is_success: boolean;
  repair_attempts: number;
  repair_history?: any[];
}

export interface VerificationResult {
  id: string;
  reproducibility_passed: boolean;
  independent_check_passed: boolean;
  math_check_passed: boolean;
  unit_check_passed: boolean;
  data_quality_check_passed: boolean;
  primary_method_result?: any;
  independent_method_result?: any;
  details?: any;
  verification_notes?: string;
}

export interface EvidenceItem {
  id: string;
  evidence_type: string;
  title: string;
  content: any;
}

export interface Proof {
  id: string;
  analysis_id: string;
  generated_code: string;
  code_language: string;
  execution_status: string;
  verification_status: 'VERIFIED' | 'PARTIALLY_VERIFIED' | 'CANNOT_DETERMINE' | 'FAILED';
  verification_score: number;
  source_datasets?: string[];
  relevant_columns?: string[];
  filters_applied?: any[];
  transformations?: string[];
  calculation_explanation?: string;
  assumptions?: string[];
  execution_result?: ExecutionResult;
  verification_result?: VerificationResult;
  evidence_items: EvidenceItem[];
}

export interface AnalysisStep {
  id: string;
  step_number: number;
  title: string;
  description?: string;
  status: 'PENDING' | 'IN_PROGRESS' | 'COMPLETED' | 'REPAIRED' | 'FAILED';
  details?: any;
}

export interface Analysis {
  id: string;
  question: string;
  dataset_ids: string[];
  status: 'PENDING' | 'IN_PROGRESS' | 'COMPLETED' | 'CANNOT_DETERMINE' | 'FAILED';
  intent?: string;
  interpreted_question?: any;
  plan_steps?: any[];
  final_answer?: string;
  refusal_reason?: string;
  verification_status: 'VERIFIED' | 'PARTIALLY_VERIFIED' | 'CANNOT_DETERMINE' | 'FAILED' | 'UNVERIFIED';
  verification_score: number;
  created_at: string;
  steps: AnalysisStep[];
  proof?: Proof;
}

export interface Relationship {
  source_dataset_id: string;
  source_column: string;
  target_dataset_id: string;
  target_column: string;
  relationship_type: string;
  confidence: number;
  warnings: string[];
}

export interface DemoQuestion {
  category: string;
  question: string;
  expected_status: string;
  target_dataset: string;
  note?: string;
}
