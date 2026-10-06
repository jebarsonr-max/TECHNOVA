from typing import Dict, Any, List

class QualityChecker:
    @staticmethod
    def generate_quality_report(profile_data: Dict[str, Any]) -> Dict[str, Any]:
        row_count = profile_data.get("row_count", 0)
        duplicate_count = profile_data.get("duplicate_count", 0)
        columns = profile_data.get("columns", [])

        issues = []
        warnings = []
        score = 100.0

        # Duplicate check
        if row_count > 0 and duplicate_count > 0:
            dup_pct = (duplicate_count / row_count) * 100
            if dup_pct > 5.0:
                issues.append(f"High duplicate rows detected: {duplicate_count} ({dup_pct:.1f}%)")
                score -= min(dup_pct, 25.0)
            else:
                warnings.append(f"Contains {duplicate_count} duplicate rows ({dup_pct:.1f}%)")
                score -= 5.0

        # Missing values check
        for col in columns:
            missing = col.get("missing_count", 0)
            if row_count > 0 and missing > 0:
                miss_pct = (missing / row_count) * 100
                if miss_pct > 20.0:
                    issues.append(f"Column '{col['name']}' has high missing values: {missing} ({miss_pct:.1f}%)")
                    score -= 10.0
                elif miss_pct > 0:
                    warnings.append(f"Column '{col['name']}' has missing values: {missing} ({miss_pct:.1f}%)")
                    score -= 2.0

            # Suspicious strings
            suspicious = col.get("suspicious_values")
            if suspicious:
                warnings.append(f"Column '{col['name']}' contains suspicious placeholder values: {suspicious}")
                score -= 3.0

        score = max(round(score, 1), 0.0)

        return {
            "quality_score": score,
            "status": "EXCELLENT" if score >= 90 else "GOOD" if score >= 75 else "NEEDS_ATTENTION" if score >= 50 else "POOR",
            "duplicate_count": duplicate_count,
            "issues": issues,
            "warnings": warnings
        }
