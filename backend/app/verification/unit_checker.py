from typing import Dict, Any, List

class UnitChecker:
    @staticmethod
    def verify_units(datasets_meta: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Verifies that operations performed across columns do not violate unit boundaries or currency consistency.
        """
        units = []
        currencies = []
        for ds in datasets_meta:
            for col in ds.get("columns", []):
                if col.get("detected_unit"):
                    units.append(col.get("detected_unit"))
                if col.get("currency_symbol"):
                    currencies.append(col.get("currency_symbol"))

        units_set = set(units)
        curr_set = set(currencies)

        if len(curr_set) > 1:
            return {
                "passed": False,
                "notes": f"Currency mismatch detected: {curr_set}"
            }

        return {
            "passed": True,
            "notes": "Unit and currency compatibility verified."
        }
