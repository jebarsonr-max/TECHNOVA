from typing import List, Dict, Any

class DatasetSchemaExtractor:
    @staticmethod
    def extract_schema_summary(dataset_meta: Dict[str, Any], columns_meta: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Extracts a clean, machine-readable schema for AI agent prompts.
        Prevents AI from hallucinating non-existent columns.
        """
        return {
            "dataset_id": dataset_meta.get("id"),
            "filename": dataset_meta.get("original_filename"),
            "row_count": dataset_meta.get("row_count"),
            "column_count": dataset_meta.get("column_count"),
            "columns": [
                {
                    "name": col["name"],
                    "type": col["detected_type"],
                    "missing": col["missing_count"],
                    "unique": col["unique_count"],
                    "min": col.get("min_value"),
                    "max": col.get("max_value"),
                    "unit": col.get("detected_unit"),
                    "currency": col.get("currency_symbol"),
                    "is_id": col.get("is_identifier", False)
                }
                for col in columns_meta
            ]
        }
