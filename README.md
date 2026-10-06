# TECHNOVA: Proof-Carrying Data Analyst (Agentic GenAI)

> **PSI Internal Qualifier Problem Statement PS08**  
> *Tagline: An AI data analyst that does not just give an answer. It gives executable proof behind the answer.*

---

## 🚀 Overview

**TECHNOVA** is a production-grade, full-stack agentic GenAI application that solves the fundamental flaw of LLM data analysis: **unverifiable answers and hallucinations**. When users upload messy real-world datasets and ask natural language analytical questions, TECHNOVA does not merely generate text. It inspects dataset schemas, constructs explicit analysis plans, generates secure analytical code, executes it inside an isolated sandbox, independently verifies results using DuckDB, and returns the answer with complete, executable proof.

If data is insufficient, ambiguous, contradictory, or unreliable, TECHNOVA enforces a strict **No-Guessing Rule**, returning `CANNOT_DETERMINE` with a transparent explanation.

---

## 🏗️ Architecture

```
[ React + TypeScript Frontend (Vite) ]
                  │
                  ▼ API Requests
[ FastAPI Backend (Python 3.14 / SQLAlchemy) ]
                  │
     ┌────────────┼───────────────────────────┐
     ▼            ▼                           ▼
[ Ingestion ]  [ Trap Detector ]      [ State Machine Pipeline ]
 & Profiler    (PS08 Traps)            - Question Analyzer
                                       - Analysis Planner
                                       - Verified Code Generator
                                       - Secure Sandbox Executor
                                       - Verification Engine (DuckDB)
                                       - Repair Loop (Up to 3x)
                                       - Evidence & Proof Builder
```

---

## 🌟 Key Features

1. **Proof-Carrying Answers**: Every numerical answer includes executable Python proof code, sandbox execution status, and DuckDB independent verification scores.
2. **PS08 Trap Detection**: Automatic refusal (`CANNOT_DETERMINE`) for:
   - Currency/Unit mismatches (USD vs EUR without exchange rate)
   - Missing required data columns (e.g. profit requested without cost column)
   - Future prediction requests on static historical data
   - Ambiguous date formats
3. **Multi-Table Analytics**: Auto-detects primary/foreign key relationships across multiple datasets and warns against row-multiplication join risks.
4. **Secure Execution Sandbox**: Analytical code executes inside isolated, network-disabled subprocesses/containers with CPU timeouts (10s) and memory caps (512 MB). Host machine is 100% protected.
5. **Self-Correction Repair Loop**: Automatically repairs code syntax/KeyErrors up to 3 times without altering original question intent.
6. **Downloadable Proof Reports**: Export complete analysis trajectory and evidence bundles in JSON/PDF formats.

---

## 🧰 Technology Stack

- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Lucide React, Recharts.
- **Backend**: Python 3.14, FastAPI, Pydantic v2, SQLAlchemy, SQLite/PostgreSQL.
- **Data Engine**: Pandas, DuckDB, PyArrow, OpenPyXL.
- **Execution & Security**: Isolated Python Subprocess Runner, Network Disabled, Resource Limits.
- **Testing**: Pytest, FastAPI TestClient.

---

## ⚙️ Quick Start & Setup

### 1. Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### 2. Backend Setup
```bash
# Clone repository
cd "HACKNEX 1"

# Create Python Virtual Environment
python -m venv venv
.\venv\Scripts\activate  # On Windows

# Install Backend Dependencies
pip install fastapi uvicorn pydantic pydantic-settings sqlalchemy pandas duckdb pyarrow openpyxl pytest httpx python-multipart python-dotenv

# Run Backend Tests
pytest -v

# Start FastAPI Backend Server
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
API OpenAPI Documentation will be live at: `http://127.0.0.1:8000/docs`

### 3. Frontend Setup
```bash
# Open new terminal
cd "HACKNEX 1/frontend"

# Install NPM Packages
npm install

# Run Frontend Production Build Check
npm run build

# Start Local Dev Server
npm run dev
```
Frontend UI will be live at: `http://localhost:5173`

---

## 🧪 Demonstration Questions

Try these built-in test questions against `data/demo/`:

| Category | Sample Question | Expected Result |
| :--- | :--- | :--- |
| **Basic Aggregation** | *What is the total order amount across all orders?* | `VERIFIED` ($77,400.50) |
| **Multi-Table Analytics** | *What is the total revenue from Enterprise segment customers?* | `VERIFIED` (Joined `orders.csv` + `customers.csv`) |
| **PS08 Trap: Missing Cost** | *What is the net profit margin for trap_missing_cost.csv?* | `CANNOT_DETERMINE` (Refused due to missing cost column) |
| **PS08 Trap: Currency Mismatch** | *What is the combined revenue from USD and EUR invoices?* | `CANNOT_DETERMINE` (Refused due to missing FX conversion rate) |

---

## 🔐 Security Declaration

- **No Exposure of Secrets**: AI API keys reside strictly on backend environment variables (`.env`).
- **No Direct Host Execution**: Generated code is scanned by `SecurityValidator` for dangerous OS/network patterns before running in restricted sandboxes.
