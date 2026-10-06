# TECHNOVA System Architecture & Design Specification

## 1. End-to-End Workflow Pipeline

```
[ User Input / CSV Upload ]
           │
           ▼
[ Data Ingestion & Profiling ]
  ├─ Immutable Raw Storage
  ├─ Column Type & Unit Detection
  ├─ Quality Report Generation
  └─ Multi-Table Relationship Detection
           │
           ▼
[ Question Analyzer & PS08 Trap Detector ]
  ├─ Intent & Required Column Mapping
  ├─ Adversarial Trap Inspection (Currency Mismatch, Missing Cost, Future Predict)
  └─ Schema Alignment Validation
           │
     ┌─────┴────────────────────────┐
     ▼                              ▼
[ Trap / Ambiguity Detected ]    [ Valid Question ]
     │                              │
     ▼                              ▼
[ CANNOT_DETERMINE Refusal ]     [ Analysis Planner ]
                                    │
                                    ▼
                                 [ Code Agent Generator ]
                                    │
                                    ▼
                                 [ Security Validator ]
                                    │
                                    ▼
                                 [ Secure Sandbox Executor ]
                                    │  (Refusal / KeyError handling)
                                    ├─► [ Self-Correction Repair Loop (Max 3x) ]
                                    │
                                    ▼
                                 [ Verification Engine ]
                                    ├─ Reproducibility Check
                                    ├─ DuckDB Independent Calculation
                                    ├─ Unit Compatibility Check
                                    └─ Data Quality Consistency Check
                                    │
                                    ▼
                                 [ Evidence & Proof Package ]
                                    └─ Return Answer + Executable Proof Card
```

## 2. Component Specifications

### Backend Services (`backend/app/`)
- `config.py`: Environment setting management via `pydantic-settings`.
- `models.py`: SQLAlchemy database schemas (`Dataset`, `Analysis`, `Proof`, `ExecutionResult`, `VerificationResult`, `Evidence`).
- `data/`: Ingestion for CSV/XLSX/JSON, profiling engine, schema extractor, relationship detector, and join path validator.
- `agents/`: Question understanding, step-by-step planner, secure code generator, and self-correction repair agent.
- `execution/`: Subprocess runner with CPU timeout (10s), memory limits (512MB), and dangerous pattern rejection.
- `verification/`: Multi-stage verification engine with DuckDB SQL cross-checking.
- `workflow/`: State machine executing all 6 workflow phases deterministically.

### Frontend Client (`frontend/src/`)
- Component-driven architecture using React 18, TypeScript, Tailwind CSS, Lucide React, and Recharts.
- Deep Proof Inspection view displaying generated analytical code, execution logs, and evidence breakdowns.
