"""End-to-end test: Upload datasets, run analysis, verify proof pipeline."""
import urllib.request
import json
import os
import sys

BASE = "http://127.0.0.1:8000"

def upload_csv(filepath: str, filename: str) -> dict:
    boundary = "TechnovaE2EBoundary9999"
    with open(filepath, "rb") as f:
        csv_bytes = f.read()

    crlf = b"\r\n"
    header = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f"Content-Type: text/csv\r\n\r\n"
    ).encode()
    footer = f"\r\n--{boundary}--\r\n".encode()
    body = header + csv_bytes + footer

    req = urllib.request.Request(
        f"{BASE}/api/datasets/upload",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def create_analysis(question: str, dataset_ids: list) -> dict:
    payload = json.dumps({"question": question, "dataset_ids": dataset_ids}).encode()
    req = urllib.request.Request(
        f"{BASE}/api/analysis",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def main():
    print("=" * 60)
    print("TECHNOVA END-TO-END VERIFICATION")
    print("=" * 60)

    demo_dir = os.path.abspath("./data/demo")

    # ── 1. Upload orders.csv ──────────────────────────────────────
    orders_path = os.path.join(demo_dir, "orders.csv")
    print("\n[1] Uploading orders.csv ...")
    ds = upload_csv(orders_path, "orders.csv")
    orders_id = ds["id"]
    print(f"    ✓ Uploaded: {ds['original_filename']} | {ds['row_count']} rows | ID: {orders_id}")
    print(f"    Quality score: {ds.get('quality_report', {}).get('overall_score', 'N/A')}")

    # ── 2. Upload customers.csv ───────────────────────────────────
    customers_path = os.path.join(demo_dir, "customers.csv")
    print("\n[2] Uploading customers.csv ...")
    ds2 = upload_csv(customers_path, "customers.csv")
    customers_id = ds2["id"]
    print(f"    ✓ Uploaded: {ds2['original_filename']} | {ds2['row_count']} rows | ID: {customers_id}")

    # ── 3. Basic sum question ─────────────────────────────────────
    question = "What is the total order amount across all orders?"
    print(f"\n[3] Running analysis: '{question}'")
    result = create_analysis(question, [orders_id])
    print(f"    Status: {result['status']}")
    print(f"    Final Answer: {result.get('final_answer')}")
    print(f"    Verification Status: {result.get('verification_status')}")
    print(f"    Verification Score: {result.get('verification_score')}")
    proof = result.get("proof", {})
    if proof:
        print(f"    Proof Execution: {proof.get('execution_status')}")
        exec_res = proof.get("execution_result", {})
        if exec_res:
            print(f"    Exec Time: {exec_res.get('execution_time_ms')} ms")
            print(f"    Repair Attempts: {exec_res.get('repair_attempts', 0)}")

    # ── 4. Average question ───────────────────────────────────────
    question2 = "What is the average order amount?"
    print(f"\n[4] Running analysis: '{question2}'")
    result2 = create_analysis(question2, [orders_id])
    print(f"    Status: {result2['status']}")
    print(f"    Final Answer: {result2.get('final_answer')}")
    print(f"    Verification Status: {result2.get('verification_status')}")

    # ── 5. Trap question (future prediction) ─────────────────────
    question3 = "Predict next month's revenue"
    print(f"\n[5] Trap test: '{question3}'")
    result3 = create_analysis(question3, [orders_id])
    print(f"    Status: {result3['status']}")
    print(f"    Final Answer: {result3.get('final_answer')}")
    trap_triggered = "CANNOT_DETERMINE" in (result3.get("final_answer") or "")
    print(f"    Trap Correctly Refused: {'✓ YES' if trap_triggered else '✗ NO'}")

    # ── 6. Count question ─────────────────────────────────────────
    question4 = "How many orders are there in total?"
    print(f"\n[6] Running analysis: '{question4}'")
    result4 = create_analysis(question4, [orders_id])
    print(f"    Status: {result4['status']}")
    print(f"    Final Answer: {result4.get('final_answer')}")

    # ── 7. Dataset list ───────────────────────────────────────────
    print("\n[7] Fetching dataset list ...")
    with urllib.request.urlopen(f"{BASE}/api/datasets") as resp:
        all_datasets = json.loads(resp.read())
    print(f"    Total datasets in DB: {len(all_datasets)}")
    for d in all_datasets:
        print(f"    - {d['original_filename']} ({d['row_count']} rows)")

    # ── 8. Analysis history ───────────────────────────────────────
    print("\n[8] Fetching analysis history ...")
    with urllib.request.urlopen(f"{BASE}/api/analysis/history") as resp:
        history = json.loads(resp.read())
    print(f"    Total analyses in history: {len(history)}")
    for h in history[:5]:
        print(f"    - [{h['status']}] {h['question'][:60]}")

    print("\n" + "=" * 60)
    print("VERIFICATION COMPLETE")
    print("=" * 60)
    print("\nAll services running:")
    print("  Backend:  http://localhost:8000")
    print("  API Docs: http://localhost:8000/docs")
    print("  Frontend: http://localhost:5173")


if __name__ == "__main__":
    main()
