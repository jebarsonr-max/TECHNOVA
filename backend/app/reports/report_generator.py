import json
from typing import Dict, Any

class ReportGenerator:
    @staticmethod
    def generate_report(analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates structured downloadable report payload for PDF / JSON export.
        """
        proof = analysis_data.get("proof", {})
        exec_res = proof.get("execution_result", {})
        ver_res = proof.get("verification_result", {})

        return {
            "title": "TECHNOVA Proof-Carrying Data Analysis Report",
            "analysis_id": analysis_data.get("id"),
            "question": analysis_data.get("question"),
            "status": analysis_data.get("status"),
            "final_answer": analysis_data.get("final_answer"),
            "verification_status": analysis_data.get("verification_status"),
            "verification_score": analysis_data.get("verification_score"),
            "refusal_reason": analysis_data.get("refusal_reason"),
            "proof_details": {
                "generated_code": proof.get("generated_code"),
                "code_language": proof.get("code_language", "python"),
                "execution_status": proof.get("execution_status"),
                "calculation_explanation": proof.get("calculation_explanation"),
                "execution_time_ms": exec_res.get("execution_time_ms")
            },
            "verification_breakdown": {
                "reproducibility": ver_res.get("reproducibility_passed"),
                "independent_cross_check": ver_res.get("independent_check_passed"),
                "unit_compatibility": ver_res.get("unit_check_passed"),
                "data_quality_support": ver_res.get("data_quality_check_passed"),
                "verification_notes": ver_res.get("verification_notes")
            },
            "evidence_list": proof.get("evidence_items", [])
        }
