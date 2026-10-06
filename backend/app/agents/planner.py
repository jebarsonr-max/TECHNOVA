from typing import List, Dict, Any

class AnalysisPlanner:
    @staticmethod
    def create_plan(interpreted_question: Dict[str, Any], datasets_schema: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Converts interpreted question into step-by-step analysis plan or refusal plan.
        """
        if interpreted_question.get("answer_type") == "CANNOT_DETERMINE" or interpreted_question.get("refusal_conditions"):
            refusal_msg = interpreted_question.get("refusal_conditions", ["CANNOT_DETERMINE: Insufficient or ambiguous data."])[0]
            return {
                "is_refusal": True,
                "refusal_reason": refusal_msg,
                "steps": [
                    {
                        "step_number": 1,
                        "action": "INSPECT_SCHEMA",
                        "description": "Inspect dataset schema and user question",
                        "parameters": {}
                    },
                    {
                        "step_number": 2,
                        "action": "REFUSE_ANALYSIS",
                        "description": f"Refuse answer due to trap/ambiguity: {refusal_msg}",
                        "parameters": {"reason": refusal_msg}
                    }
                ]
            }

        steps = [
            {
                "step_number": 1,
                "action": "LOAD_DATASETS",
                "description": f"Load dataset(s): {', '.join(interpreted_question.get('required_datasets', []))}",
                "parameters": {"datasets": interpreted_question.get("required_datasets", [])}
            },
            {
                "step_number": 2,
                "action": "CLEAN_AND_FILTER",
                "description": "Apply data cleaning, handle missing values, and apply filters",
                "parameters": {"required_columns": interpreted_question.get("required_columns", [])}
            }
        ]

        if len(interpreted_question.get("required_datasets", [])) > 1:
            steps.append({
                "step_number": 3,
                "action": "JOIN_DATASETS",
                "description": "Join multiple tables on primary key / foreign key relationship",
                "parameters": {"join_type": "INNER"}
            })

        steps.append({
            "step_number": len(steps) + 1,
            "action": "EXECUTE_CALCULATION",
            "description": f"Calculate {interpreted_question.get('intent', 'metric')} on target columns",
            "parameters": {"metric": interpreted_question.get("metric")}
        })

        steps.append({
            "step_number": len(steps) + 1,
            "action": "VERIFY_AND_CROSS_CHECK",
            "description": "Cross-check result with independent calculation engine",
            "parameters": {"method": "DUCKDB_CROSS_CHECK"}
        })

        return {
            "is_refusal": False,
            "refusal_reason": None,
            "steps": steps
        }
