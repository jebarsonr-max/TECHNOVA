import os
from typing import List, Dict, Any

class CodeAgent:
    @staticmethod
    def generate_proof_code(
        question: str,
        plan: Dict[str, Any],
        datasets_meta: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generates deterministic, secure analytical Python/DuckDB code based on actual schemas.
        Output must contain NO network access, NO OS calls, NO unsafe imports.
        """
        if plan.get("is_refusal"):
            refusal_reason = plan.get("refusal_reason", "CANNOT_DETERMINE")
            code = f"""# REFUSAL CODE
# Reason: {refusal_reason}
import json
result = {{"status": "CANNOT_DETERMINE", "reason": "{refusal_reason}"}}
print(json.dumps(result))
"""
            return {
                "language": "python",
                "code": code,
                "expected_output_type": "CANNOT_DETERMINE",
                "explanation": f"Refused calculation: {refusal_reason}"
            }

        # Build clean Python analytical script for execution sandbox
        dataset_loading_lines = []
        df_vars = []

        for idx, ds in enumerate(datasets_meta):
            var_name = f"df_{idx+1}"
            df_vars.append(var_name)
            file_path = ds.get("file_path", "").replace("\\", "/")
            file_type = ds.get("file_type", "csv").lower()

            if file_type in ["csv", "txt"]:
                load_cmd = f"pd.read_csv('{file_path}')"
            elif file_type in ["xlsx", "xls"]:
                load_cmd = f"pd.read_excel('{file_path}')"
            elif file_type == "json":
                load_cmd = f"pd.read_json('{file_path}')"
            else:
                load_cmd = f"pd.read_csv('{file_path}')"

            dataset_loading_lines.append(f"{var_name} = {load_cmd}")

        q_lower = question.lower()
        
        # Determine exact metric calculation
        calculation_logic = ""
        if len(df_vars) == 1:
            main_df = df_vars[0]
            cols = datasets_meta[0].get("columns", [])
            numeric_cols = [c["name"] for c in cols if c.get("detected_type") in ["float", "integer", "numeric"]]
            
            # Match numeric column from question
            matched_col = None
            for nc in numeric_cols:
                if nc.lower() in q_lower:
                    matched_col = nc
                    break
            if not matched_col and numeric_cols:
                matched_col = numeric_cols[0]

            if matched_col:
                if "average" in q_lower or "avg" in q_lower or "mean" in q_lower:
                    calc_expr = f"float({main_df}['{matched_col}'].dropna().mean())"
                    method_name = "average"
                elif "count" in q_lower or "how many" in q_lower:
                    calc_expr = f"int({main_df}['{matched_col}'].dropna().count())"
                    method_name = "count"
                else:
                    calc_expr = f"float({main_df}['{matched_col}'].dropna().sum())"
                    method_name = "sum"

                calculation_logic = f"""
col_target = '{matched_col}'
value = {calc_expr}
final_result = {{
    "answer": round(value, 4),
    "metric": "{method_name}",
    "column": col_target,
    "row_count": len({main_df}),
    "datasets": ["{datasets_meta[0].get('original_filename')}"]
}}
"""
            else:
                calculation_logic = f"""
final_result = {{
    "answer": len({main_df}),
    "metric": "row_count",
    "datasets": ["{datasets_meta[0].get('original_filename')}"]
}}
"""
        else:
            # Multi-table join code generation
            df1, df2 = df_vars[0], df_vars[1]
            cols1 = [c["name"] for c in datasets_meta[0].get("columns", [])]
            cols2 = [c["name"] for c in datasets_meta[1].get("columns", [])]
            common = list(set(cols1).intersection(set(cols2)))
            join_col = common[0] if common else "id"

            calculation_logic = f"""
merged_df = pd.merge({df1}, {df2}, on='{join_col}', how='inner')
# Perform calculation on merged set
numeric_cols = merged_df.select_dtypes(include=[np.number]).columns.tolist()
calc_col = numeric_cols[0] if numeric_cols else '{join_col}'
ans_val = float(merged_df[calc_col].sum()) if numeric_cols else len(merged_df)

final_result = {{
    "answer": round(ans_val, 4),
    "metric": "multi_table_sum",
    "join_column": "{join_col}",
    "row_count": len(merged_df),
    "datasets": ["{datasets_meta[0].get('original_filename')}", "{datasets_meta[1].get('original_filename')}"]
}}
"""

        code = f"""import pandas as pd
import numpy as np
import json

# --- SECURE EXECUTABLE PROOF SCRIPT ---
# Step 1: Load Immutable Source Data
{os.linesep.join(dataset_loading_lines)}

# Step 2: Executable Analytical Calculation
{calculation_logic}

# Step 3: Structured Proof Output
print(json.dumps(final_result))
"""

        return {
            "language": "python",
            "code": code,
            "expected_output_type": "NUMBER",
            "explanation": f"Generated executable Python proof code targeting {len(datasets_meta)} dataset(s)."
        }
