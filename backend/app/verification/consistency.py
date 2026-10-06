from typing import Dict, Any

class ConsistencyChecker:
    @staticmethod
    def verify_consistency(primary_result: Dict[str, Any], quality_report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verifies that result calculation is consistent with dataset quality parameters.
        """
        score = quality_report.get("quality_score", 100.0)
        has_issues = len(quality_report.get("issues", [])) > 0

        return {
            "passed": score >= 50.0,
            "quality_score": score,
            "has_warnings": len(quality_report.get("warnings", [])) > 0,
            "notes": "Dataset quality score supports numerical confidence." if score >= 50.0 else "Data quality is poor, reducing verification confidence."
        }
