from typing import Dict, Any, List

class EvidenceBuilder:
    @staticmethod
    def build_evidence(
        execution_result: Dict[str, Any],
        verification_result: Dict[str, Any],
        datasets_meta: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Builds transparent, verifiable evidence items supporting the final numerical answer.
        """
        evidence_items = []
        result_data = execution_result.get("result_data", {})

        # Evidence 1: Calculation Metric Summary
        evidence_items.append({
            "evidence_type": "METRIC_SUMMARY",
            "title": "Calculated Result Summary",
            "content": {
                "answer": result_data.get("answer"),
                "metric": result_data.get("metric"),
                "target_column": result_data.get("column"),
                "row_count_analyzed": result_data.get("row_count")
            }
        })

        # Evidence 2: Source Dataset Proof
        evidence_items.append({
            "evidence_type": "SOURCE_PROOF",
            "title": "Immutable Source Datasets",
            "content": {
                "source_files": [ds.get("original_filename") for ds in datasets_meta],
                "row_counts": {ds.get("original_filename"): ds.get("row_count") for ds in datasets_meta}
            }
        })

        # Evidence 3: Independent Cross-Check Verification
        evidence_items.append({
            "evidence_type": "CROSS_CHECK",
            "title": "DuckDB Independent Verification",
            "content": {
                "reproducibility_passed": verification_result.get("reproducibility_passed"),
                "math_check_passed": verification_result.get("math_check_passed"),
                "independent_answer": verification_result.get("independent_method_result")
            }
        })

        return evidence_items
