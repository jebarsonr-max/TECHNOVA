import pandas as pd
from typing import List, Dict, Any

class RelationshipDetector:
    @staticmethod
    def detect_relationships(datasets: List[Dict[str, Any]], dataframes: Dict[str, pd.DataFrame]) -> List[Dict[str, Any]]:
        """
        Detects primary key -> foreign key candidates and relationships between multiple datasets.
        """
        relationships = []

        dataset_ids = list(dataframes.keys())
        for i in range(len(dataset_ids)):
            for j in range(i + 1, len(dataset_ids)):
                ds1_id = dataset_ids[i]
                ds2_id = dataset_ids[j]

                df1 = dataframes[ds1_id]
                df2 = dataframes[ds2_id]

                # Match column names
                common_cols = set(df1.columns).intersection(set(df2.columns))

                for col in common_cols:
                    s1 = df1[col].dropna()
                    s2 = df2[col].dropna()

                    if s1.empty or s2.empty:
                        continue

                    # Uniqueness checks
                    u1 = s1.nunique() == len(df1)
                    u2 = s2.nunique() == len(df2)

                    overlap = len(set(s1).intersection(set(s2)))
                    min_unique = min(s1.nunique(), s2.nunique())

                    if min_unique > 0 and (overlap / min_unique) > 0.3:
                        if u1 and not u2:
                            rel_type = "one_to_many"
                            src_id, tgt_id = ds1_id, ds2_id
                        elif u2 and not u1:
                            rel_type = "one_to_many"
                            src_id, tgt_id = ds2_id, ds1_id
                        elif u1 and u2:
                            rel_type = "one_to_one"
                            src_id, tgt_id = ds1_id, ds2_id
                        else:
                            rel_type = "many_to_many"
                            src_id, tgt_id = ds1_id, ds2_id

                        warnings = []
                        if rel_type == "many_to_many":
                            warnings.append("Risk of row multiplication during join due to many-to-many relationship.")

                        confidence = round(overlap / min_unique, 2)
                        relationships.append({
                            "source_dataset_id": src_id,
                            "source_column": col,
                            "target_dataset_id": tgt_id,
                            "target_column": col,
                            "relationship_type": rel_type,
                            "confidence": confidence,
                            "warnings": warnings
                        })

        return relationships
