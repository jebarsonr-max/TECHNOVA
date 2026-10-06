import pandas as pd
import numpy as np
import re
from typing import Dict, Any, List

CURRENCY_REGEX = re.compile(r'[\$€£₹¥]')
DATE_PATTERNS = [
    r'^\d{4}-\d{2}-\d{2}$',
    r'^\d{2}/\d{2}/\d{4}$',
    r'^\d{2}-\d{2}-\d{4}$',
]

class DataProfiler:
    @staticmethod
    def profile(df: pd.DataFrame) -> Dict[str, Any]:
        row_count = len(df)
        column_count = len(df.columns)
        duplicate_count = int(df.duplicated().sum())

        columns_profile = []
        date_columns = []
        categorical_columns = []
        numeric_columns = []

        for col in df.columns:
            series = df[col]
            missing_count = int(series.isna().sum())
            unique_count = int(series.nunique(dropna=True))

            # Sample non-null values
            valid_samples = series.dropna().astype(str).head(100).tolist()
            
            # Detect Data Type & Unit / Currency
            detected_type, currency, unit, is_id, suspicious = DataProfiler._inspect_column(series, col, valid_samples)

            min_val = None
            max_val = None
            mean_val = None

            if detected_type in ["numeric", "integer", "float"]:
                numeric_columns.append(col)
                numeric_series = pd.to_numeric(series, errors='coerce')
                if not numeric_series.dropna().empty:
                    min_val = str(round(float(numeric_series.min()), 4))
                    max_val = str(round(float(numeric_series.max()), 4))
                    mean_val = round(float(numeric_series.mean()), 4)
            elif detected_type == "date":
                date_columns.append(col)
                if valid_samples:
                    min_val = str(valid_samples[0])
                    max_val = str(valid_samples[-1])
            else:
                categorical_columns.append(col)
                if valid_samples:
                    min_val = str(valid_samples[0])
                    max_val = str(valid_samples[-1])

            columns_profile.append({
                "name": col,
                "data_type": str(series.dtype),
                "detected_type": detected_type,
                "missing_count": missing_count,
                "unique_count": unique_count,
                "min_value": min_val,
                "max_value": max_val,
                "mean_value": mean_val,
                "currency_symbol": currency,
                "detected_unit": unit,
                "is_identifier": is_id,
                "suspicious_values": suspicious
            })

        return {
            "row_count": row_count,
            "column_count": column_count,
            "duplicate_count": duplicate_count,
            "columns": columns_profile,
            "date_columns": date_columns,
            "categorical_columns": categorical_columns,
            "numeric_columns": numeric_columns
        }

    @staticmethod
    def _inspect_column(series: pd.Series, col_name: str, samples: List[str]) -> tuple:
        currency = None
        unit = None
        is_id = False
        suspicious = []

        # Identifier check
        if col_name.lower().endswith(('_id', 'id', 'key', 'code')) or (series.nunique() == len(series) and len(series) > 0):
            is_id = True

        # Currency check
        for sample in samples:
            match = CURRENCY_REGEX.search(sample)
            if match:
                currency = match.group(0)
                break
        
        # Unit detection in column name or values
        col_lower = col_name.lower()
        if 'usd' in col_lower or '$' in col_lower:
            currency = '$'
            unit = 'USD'
        elif 'eur' in col_lower or '€' in col_lower:
            currency = '€'
            unit = 'EUR'
        elif 'inr' in col_lower or '₹' in col_lower:
            currency = '₹'
            unit = 'INR'
        elif 'kg' in col_lower or 'kilogram' in col_lower:
            unit = 'kg'
        elif 'pct' in col_lower or 'percent' in col_lower or '%' in col_lower:
            unit = '%'

        # Type detection
        non_nulls = series.dropna()
        if non_nulls.empty:
            return "unknown", currency, unit, is_id, suspicious

        # Check numeric
        try:
            converted = pd.to_numeric(non_nulls)
            if (converted % 1 == 0).all():
                detected_type = "integer"
            else:
                detected_type = "float"
        except (ValueError, TypeError):
            # Check date
            is_date = False
            try:
                pd.to_datetime(non_nulls.head(20), format='mixed', errors='raise')
                is_date = True
            except Exception:
                pass
            
            if is_date or any(keyword in col_lower for keyword in ['date', 'time', 'timestamp', 'created_at', 'updated_at', 'year', 'month']):
                detected_type = "date"
            else:
                detected_type = "categorical"

        # Check for suspicious values
        for val in samples:
            if val.lower() in ['n/a', 'na', 'null', 'undefined', 'missing', 'none', '?', 'unk', 'unknown', '-999', '9999']:
                suspicious.append(val)

        return detected_type, currency, unit, is_id, suspicious
