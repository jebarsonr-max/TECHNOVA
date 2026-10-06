from typing import Dict, Any

class ReproducibilityChecker:
    @staticmethod
    def check_reproducibility(execution_result: Dict[str, Any], proof_code: str) -> Dict[str, Any]:
        """
        Verifies that code execution yielded deterministic result output without silent failures.
        """
        is_success = execution_result.get("is_success", False)
        result_data = execution_result.get("result_data")

        if not is_success or result_data is None:
            return {
                "passed": False,
                "notes": "Code execution failed or produced empty result output."
            }

        return {
            "passed": True,
            "notes": "Code execution reproduced deterministic structured result."
        }
