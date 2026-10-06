import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from backend.app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(String, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)  # csv, xlsx, json
    file_size_bytes = Column(Integer, nullable=False)
    file_path = Column(String, nullable=False)
    row_count = Column(Integer, default=0)
    column_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Profiling & Quality metadata
    profiling_summary = Column(JSON, nullable=True)
    quality_report = Column(JSON, nullable=True)

    columns = relationship("DatasetColumn", back_populates="dataset", cascade="all, delete-orphan")

class DatasetColumn(Base):
    __tablename__ = "dataset_columns"

    id = Column(String, primary_key=True, index=True)
    dataset_id = Column(String, ForeignKey("datasets.id"), nullable=False)
    name = Column(String, nullable=False)
    data_type = Column(String, nullable=False)  # numeric, categorical, date, boolean, id
    detected_type = Column(String, nullable=False)
    missing_count = Column(Integer, default=0)
    unique_count = Column(Integer, default=0)
    min_value = Column(String, nullable=True)
    max_value = Column(String, nullable=True)
    mean_value = Column(Float, nullable=True)
    currency_symbol = Column(String, nullable=True)
    detected_unit = Column(String, nullable=True)
    is_identifier = Column(Boolean, default=False)
    suspicious_values = Column(JSON, nullable=True)

    dataset = relationship("Dataset", back_populates="columns")

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(String, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    dataset_ids = Column(JSON, nullable=False)  # List of dataset IDs referenced
    status = Column(String, default="PENDING")  # PENDING, IN_PROGRESS, COMPLETED, CANNOT_DETERMINE, FAILED
    
    # Interpretation & Plan
    intent = Column(String, nullable=True)
    interpreted_question = Column(JSON, nullable=True)
    plan_steps = Column(JSON, nullable=True)
    
    # Final Answer
    final_answer = Column(Text, nullable=True)
    refusal_reason = Column(Text, nullable=True)
    
    # Status indicators
    verification_status = Column(String, default="UNVERIFIED")  # VERIFIED, PARTIALLY_VERIFIED, CANNOT_DETERMINE, FAILED
    verification_score = Column(Float, default=0.0)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    steps = relationship("AnalysisStep", back_populates="analysis", cascade="all, delete-orphan")
    proof = relationship("Proof", back_populates="analysis", uselist=False, cascade="all, delete-orphan")

class AnalysisStep(Base):
    __tablename__ = "analysis_steps"

    id = Column(String, primary_key=True, index=True)
    analysis_id = Column(String, ForeignKey("analyses.id"), nullable=False)
    step_number = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, default="PENDING")  # PENDING, IN_PROGRESS, COMPLETED, REPAIRED, FAILED
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    analysis = relationship("Analysis", back_populates="steps")

class Proof(Base):
    __tablename__ = "proofs"

    id = Column(String, primary_key=True, index=True)
    analysis_id = Column(String, ForeignKey("analyses.id"), nullable=False, unique=True)
    generated_code = Column(Text, nullable=False)
    code_language = Column(String, default="python")  # python, duckdb
    
    execution_status = Column(String, default="NOT_EXECUTED")  # SUCCESS, FAILED, TIMEOUT, SECURITY_VIOLATION
    verification_status = Column(String, default="UNVERIFIED")
    verification_score = Column(Float, default=0.0)

    # Breakdown for display
    source_datasets = Column(JSON, nullable=True)
    relevant_columns = Column(JSON, nullable=True)
    filters_applied = Column(JSON, nullable=True)
    transformations = Column(JSON, nullable=True)
    calculation_explanation = Column(Text, nullable=True)
    assumptions = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    analysis = relationship("Analysis", back_populates="proof")
    execution_result = relationship("ExecutionResult", back_populates="proof", uselist=False, cascade="all, delete-orphan")
    verification_result = relationship("VerificationResult", back_populates="proof", uselist=False, cascade="all, delete-orphan")
    evidence_items = relationship("Evidence", back_populates="proof", cascade="all, delete-orphan")

class ExecutionResult(Base):
    __tablename__ = "execution_results"

    id = Column(String, primary_key=True, index=True)
    proof_id = Column(String, ForeignKey("proofs.id"), nullable=False, unique=True)
    exit_code = Column(Integer, default=0)
    stdout = Column(Text, nullable=True)
    stderr = Column(Text, nullable=True)
    execution_time_ms = Column(Float, default=0.0)
    result_data = Column(JSON, nullable=True)  # Raw numerical/table result
    is_success = Column(Boolean, default=False)
    repair_attempts = Column(Integer, default=0)
    repair_history = Column(JSON, nullable=True)

    proof = relationship("Proof", back_populates="execution_result")

class VerificationResult(Base):
    __tablename__ = "verification_results"

    id = Column(String, primary_key=True, index=True)
    proof_id = Column(String, ForeignKey("proofs.id"), nullable=False, unique=True)
    reproducibility_passed = Column(Boolean, default=False)
    independent_check_passed = Column(Boolean, default=False)
    math_check_passed = Column(Boolean, default=False)
    unit_check_passed = Column(Boolean, default=False)
    data_quality_check_passed = Column(Boolean, default=False)

    primary_method_result = Column(JSON, nullable=True)
    independent_method_result = Column(JSON, nullable=True)

    details = Column(JSON, nullable=True)
    verification_notes = Column(Text, nullable=True)

    proof = relationship("Proof", back_populates="verification_result")

class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(String, primary_key=True, index=True)
    proof_id = Column(String, ForeignKey("proofs.id"), nullable=False)
    evidence_type = Column(String, nullable=False)  # SAMPLE_ROWS, METRIC_SUMMARY, CROSS_CHECK, QUALITY_NOTE
    title = Column(String, nullable=False)
    content = Column(JSON, nullable=False)

    proof = relationship("Proof", back_populates="evidence_items")
