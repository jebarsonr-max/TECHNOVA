import json
from typing import List, Dict, Any
from backend.app.verification.trap_detector import PS08TrapDetector

class QuestionAnalyzer:
    @staticmethod
    def analyze_question(question: str, datasets_schema: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Converts natural language question into structured analysis requirements.
        Validates schema, detects missing columns, ambiguities, and PS08 trap conditions.
        """
        # Step 1: Check PS08 Adversarial Traps
        trap_result = PS08TrapDetector.inspect_for_traps(question, datasets_schema)
        if trap_result["has_trap"]:
            return {
                "intent": "REFUSAL",
                "metric": None,
                "dimensions": [],
                "filters": [],
                "required_columns": [],
                "required_datasets": [ds.get("dataset_id") for ds in datasets_schema],
                "ambiguities": [trap_result["refusal_reason"]],
                "answer_type": "CANNOT_DETERMINE",
                "refusal_conditions": [trap_result["refusal_reason"]]
            }

        # Step 2: Extract requested columns & intent heuristics
        all_cols_map = {}
        for ds in datasets_schema:
            for col in ds.get("columns", []):
                all_cols_map[col["name"].lower()] = (ds.get("dataset_id"), col["name"])

        q_lower = question.lower()
        required_cols = []
        required_ds_ids = set()

        for col_name_lower, (ds_id, orig_col) in all_cols_map.items():
            if col_name_lower in q_lower:
                required_cols.append(orig_col)
                required_ds_ids.add(ds_id)

        # Detect intent
        intent = "AGGREGATION"
        metric = None
        if "total" in q_lower or "sum" in q_lower or "revenue" in q_lower or "sales" in q_lower:
            intent = "SUM_AGGREGATION"
            metric = "SUM"
        elif "average" in q_lower or "avg" in q_lower or "mean" in q_lower:
            intent = "AVERAGE_AGGREGATION"
            metric = "AVERAGE"
        elif "count" in q_lower or "how many" in q_lower or "number of" in q_lower:
            intent = "COUNT_AGGREGATION"
            metric = "COUNT"
        elif "top" in q_lower or "highest" in q_lower or "best" in q_lower:
            intent = "RANKING"
            metric = "RANK"
        elif "compare" in q_lower or "difference" in q_lower:
            intent = "COMPARISON"
            metric = "DIFFERENCE"

        # Check column existence
        if not required_cols and datasets_schema:
            # Pick primary numeric or default columns if generic question
            for ds in datasets_schema:
                for col in ds.get("columns", []):
                    if col.get("type") in ["float", "integer", "numeric"] and not metric:
                        required_cols.append(col["name"])
                        required_ds_ids.add(ds.get("dataset_id"))
                        break

        if not required_ds_ids:
            required_ds_ids = {ds.get("dataset_id") for ds in datasets_schema}

        return {
            "intent": intent,
            "metric": metric,
            "dimensions": [],
            "filters": [],
            "date_ranges": None,
            "grouping": [],
            "sorting": None,
            "required_columns": list(set(required_cols)),
            "required_datasets": list(required_ds_ids),
            "ambiguities": [],
            "answer_type": "NUMBER",
            "refusal_conditions": []
        }
