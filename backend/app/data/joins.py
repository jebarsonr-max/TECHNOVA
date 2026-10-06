from typing import List, Dict, Any

class JoinValidator:
    @staticmethod
    def validate_join_plan(joins: List[Dict[str, Any]], relationships: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validates join execution paths and warns if joins are unsafe or might multiply rows.
        """
        warnings = []
        is_safe = True

        rel_lookup = {
            (r["source_dataset_id"], r["target_dataset_id"], r["source_column"]): r["relationship_type"]
            for r in relationships
        }
        # Also reverse
        rel_lookup.update({
            (r["target_dataset_id"], r["source_dataset_id"], r["target_column"]): r["relationship_type"]
            for r in relationships
        })

        for j in joins:
            ds1 = j.get("left_dataset")
            ds2 = j.get("right_dataset")
            col = j.get("on_column")

            rel_type = rel_lookup.get((ds1, ds2, col), "unknown")
            if rel_type == "many_to_many":
                warnings.append(f"Joining {ds1} and {ds2} on '{col}' is many-to-many. Row count will multiply.")
                is_safe = False
            elif rel_type == "unknown":
                warnings.append(f"No direct relationship detected between {ds1} and {ds2} on '{col}'. Join may yield empty or invalid results.")

        return {
            "is_safe": is_safe,
            "warnings": warnings
        }
