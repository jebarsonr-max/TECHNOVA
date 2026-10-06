from typing import Dict, Any, List
from backend.app.verification.reproducibility import ReproducibilityChecker
from backend.app.verification.math_checker import MathChecker
from backend.app.verification.unit_checker import UnitChecker
from backend.app.verification.consistency import ConsistencyChecker

class VerificationEngine:
    @staticmethod
    def verify(
        execution_result: Dict[str, Any],
        proof_code: str,
        datasets_meta: List[Dict[str, Any]],
        quality_report: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Runs comprehensive verification suite on execution result.
        Returns verification status (VERIFIED, PARTIALLY_VERIFIED, CANNOT_DETERMINE, FAILED) and score.
        """
        result_data = execution_result.get("result_data", {})
        if isinstance(result_data, dict) and result_data.get("status") == "CANNOT_DETERMINE":
            return {
                "verification_status": "CANNOT_DETERMINE",
                "verification_score": 0.0,
                "reproducibility_passed": False,
                "independent_check_passed": False,
                "math_check_passed": False,
                "unit_check_passed": False,
                "data_quality_check_passed": False,
                "primary_method_result": result_data,
                "independent_method_result": None,
                "notes": result_data.get("reason", "Refused answer due to insufficient or ambiguous data.")
            }

        # 1. Reproducibility
        rep_res = ReproducibilityChecker.check_reproducibility(execution_result, proof_code)
        
        # 2. Math check (DuckDB cross-check)
        math_res = MathChecker.verify_with_duckdb(result_data, datasets_meta)
        
        # 3. Unit check
        unit_res = UnitChecker.verify_units(datasets_meta)
        
        # 4. Consistency check
        cons_res = ConsistencyChecker.verify_consistency(result_data, quality_report)

        # Compute Score
        passed_count = sum([rep_res["passed"], math_res["passed"], unit_res["passed"], cons_res["passed"]])
        score = round(passed_count / 4.0, 2)

        if score >= 0.9 and rep_res["passed"] and execution_result.get("is_success"):
            status = "VERIFIED"
        elif score >= 0.6:
            status = "PARTIALLY_VERIFIED"
        elif not execution_result.get("is_success"):
            status = "FAILED"
        else:
            status = "CANNOT_DETERMINE"

        return {
            "verification_status": status,
            "verification_score": score,
            "reproducibility_passed": rep_res["passed"],
            "independent_check_passed": math_res["passed"],
            "math_check_passed": math_res["passed"],
            "unit_check_passed": unit_res["passed"],
            "data_quality_check_passed": cons_res["passed"],
            "primary_method_result": result_data,
            "independent_method_result": math_res.get("independent_answer"),
            "notes": f"Verification completed with status {status} (score: {score}). {math_res.get('reason', '')}"
        }
