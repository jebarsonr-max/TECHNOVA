from typing import List, Dict, Any

class PS08TrapDetector:
    @staticmethod
    def inspect_for_traps(question: str, datasets_schema: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Inspects the question and dataset schemas for PS08 adversarial trap conditions.
        Returns trap flags and refusal reasons if present.
        """
        q_lower = question.lower()
        has_trap = False
        refusal_reason = ""
        trap_type = None

        all_cols = []
        col_units = {}
        for ds in datasets_schema:
            for col in ds.get("columns", []):
                all_cols.append(col["name"].lower())
                if col.get("unit"):
                    col_units[col["name"].lower()] = col.get("unit")
                if col.get("currency"):
                    col_units[col["name"].lower()] = col.get("currency")

        # 1. Missing data trap (e.g. Profit requested but Cost column missing)
        if any(term in q_lower for term in ["profit", "margin", "net income"]) and "cost" not in all_cols and "expense" not in all_cols and "profit" not in all_cols:
            has_trap = True
            trap_type = "MISSING_DATA"
            refusal_reason = "CANNOT_DETERMINE: Profit calculation requested, but required 'cost' or 'expense' column is missing from the provided dataset."

        # 2. Currency/Unit mismatch trap (e.g. Revenue in USD, Cost in EUR without conversion rate)
        units_set = set(col_units.values())
        if len(units_set) > 1 and any(u in ["USD", "$", "EUR", "€"] for u in units_set):
            if "$" in units_set and "€" in units_set or "USD" in units_set and "EUR" in units_set:
                has_trap = True
                trap_type = "CURRENCY_MISMATCH"
                refusal_reason = "CANNOT_DETERMINE: Currency mismatch detected (USD vs EUR) without an explicit exchange rate table or conversion factor."

        # 3. Future prediction / Forecasting trap
        if any(term in q_lower for term in ["next year", "future revenue", "predict", "forecast", "tomorrow"]) and not any(term in q_lower for term in ["history", "trend"]):
            has_trap = True
            trap_type = "FUTURE_DATA_TRAP"
            refusal_reason = "CANNOT_DETERMINE: Future prediction or forecasting requested, but dataset contains only historical records and no predictive model is available."

        # 4. Ambiguous date trap (e.g. asking for 'last year' when date column is absent)
        if any(term in q_lower for term in ["last year", "month", "quarter", "annual"]) and not any(ds.get("columns") for ds in datasets_schema if any(c.get("type") == "date" or "date" in c.get("name").lower() for c in ds.get("columns", []))):
            has_trap = True
            trap_type = "AMBIGUOUS_DATE"
            refusal_reason = "CANNOT_DETERMINE: Time-based comparison requested ('last year' / 'month'), but no date column was found in the dataset."

        return {
            "has_trap": has_trap,
            "trap_type": trap_type,
            "refusal_reason": refusal_reason
        }
