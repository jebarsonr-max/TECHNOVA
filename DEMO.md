# TECHNOVA Demonstration Guide

Follow this live demo flow to demonstrate all PS08 requirements to judges:

## Step 1: Launch Backend & Frontend
1. Start Backend: `uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload`
2. Start Frontend: `cd frontend && npm run dev`
3. Open browser at `http://localhost:5173`

## Step 2: Upload Datasets & View Profiling
1. Go to **Datasets** page.
2. Drag & drop synthetic demo datasets from `data/demo/`:
   - `orders.csv`
   - `customers.csv`
   - `trap_missing_cost.csv`
   - `trap_currency_mismatch.csv`
3. Click on `orders.csv` -> **Profile** to view data quality score, missing values, and column data types.

## Step 3: Run Valid Aggregation & Multi-Table Questions
1. Go to **Analytics Studio** (Dashboard).
2. Click live demo question: *"What is the total order amount across all orders?"*
3. View the **Answer Card** ($77,400.50), **VERIFIED PROOF** badge, generated Python code, and DuckDB cross-check result.
4. Click **Inspect Proof** to view the deep proof card and evidence bundle.

## Step 4: Run PS08 Adversarial Trap Questions
1. Select `trap_missing_cost.csv` and ask: *"What is the net profit margin for transactions?"*
2. System detects missing cost column and returns **`CANNOT_DETERMINE`** refusal with explanation.
3. Select `trap_currency_mismatch.csv` and ask: *"What is the total combined revenue?"*
4. System detects USD vs EUR currency mismatch without FX table and returns **`CANNOT_DETERMINE`** refusal.
