from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# --- Dataset Schemas ---
class DatasetColumnSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    data_type: str
    detected_type: str
    missing_count: int
    unique_count: int
    min_value: Optional[str] = None
    max_value: Optional[str] = None
    mean_value: Optional[float] = None
    currency_symbol: Optional[str] = None
    detected_unit: Optional[str] = None
    is_identifier: bool = False
    suspicious_values: Optional[List[Any]] = None

class DatasetSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    filename: str
    original_filename: str
    file_type: str
    file_size_bytes: int
    row_count: int
    column_count: int
    created_at: datetime
    columns: List[DatasetColumnSchema] = []
    profiling_summary: Optional[Dict[str, Any]] = None
    quality_report: Optional[Dict[str, Any]] = None

# --- Analysis Schemas ---
class QuestionRequest(BaseModel):
    question: str
    dataset_ids: List[str]

class QuestionInterpretation(BaseModel):
    intent: str
    metric: Optional[str] = None
    dimensions: List[str] = []
    filters: List[Dict[str, Any]] = []
    date_ranges: Optional[Dict[str, Any]] = None
    grouping: List[str] = []
    sorting: Optional[Dict[str, Any]] = None
    comparison_requirements: Optional[Dict[str, Any]] = None
    required_columns: List[str] = []
    required_datasets: List[str] = []
    ambiguities: List[str] = []
    answer_type: str = "NUMBER"  # NUMBER, TABLE, REFUSAL, TEXT
    refusal_conditions: List[str] = []

class AnalysisPlanStep(BaseModel):
    step_number: int
    action: str  # load, filter, join, group, aggregate, compare, verify, evidence
    description: str
    parameters: Dict[str, Any] = {}

class ExecutionResultSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    exit_code: int
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    execution_time_ms: float
    result_data: Optional[Dict[str, Any]] = None
    is_success: bool
    repair_attempts: int = 0
    repair_history: Optional[List[Dict[str, Any]]] = None

class VerificationResultSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    reproducibility_passed: bool
    independent_check_passed: bool
    math_check_passed: bool
    unit_check_passed: bool
    data_quality_check_passed: bool
    primary_method_result: Optional[Any] = None
    independent_method_result: Optional[Any] = None
    details: Optional[Dict[str, Any]] = None
    verification_notes: Optional[str] = None

class EvidenceSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    evidence_type: str
    title: str
    content: Dict[str, Any]

class ProofSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    analysis_id: str
    generated_code: str
    code_language: str
    execution_status: str
    verification_status: str
    verification_score: float
    source_datasets: Optional[List[str]] = None
    relevant_columns: Optional[List[str]] = None
    filters_applied: Optional[List[Dict[str, Any]]] = None
    transformations: Optional[List[str]] = None
    calculation_explanation: Optional[str] = None
    assumptions: Optional[List[str]] = None
    execution_result: Optional[ExecutionResultSchema] = None
    verification_result: Optional[VerificationResultSchema] = None
    evidence_items: List[EvidenceSchema] = []

class AnalysisStepSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    step_number: int
    title: str
    description: Optional[str] = None
    status: str
    details: Optional[Dict[str, Any]] = None

class AnalysisResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    question: str
    dataset_ids: List[str]
    status: str
    intent: Optional[str] = None
    interpreted_question: Optional[Dict[str, Any]] = None
    plan_steps: Optional[List[Dict[str, Any]]] = None
    final_answer: Optional[str] = None
    refusal_reason: Optional[str] = None
    verification_status: str
    verification_score: float
    created_at: datetime
    steps: List[AnalysisStepSchema] = []
    proof: Optional[ProofSchema] = None

# --- Multi-table Relationship Schemas ---
class RelationshipSchema(BaseModel):
    source_dataset_id: str
    source_column: str
    target_dataset_id: str
    target_column: str
    relationship_type: str  # one_to_one, one_to_many, many_to_many
    confidence: float
    warnings: List[str] = []
