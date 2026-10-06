import os
import pandas as pd
import duckdb
from typing import Tuple, Dict, Any

class DataIngestionEngine:
    @staticmethod
    def load_dataset(file_path: str, file_type: str) -> pd.DataFrame:
        """
        Loads CSV, XLSX, or JSON into a pandas DataFrame cleanly while leaving the source file untouched (immutable).
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Dataset file not found at {file_path}")

        file_type = file_type.lower().strip(".")

        if file_type == "csv":
            # Try reading with pandas, auto-detect separator if needed
            try:
                df = pd.read_csv(file_path)
            except Exception:
                df = pd.read_csv(file_path, sep=None, engine='python')
        elif file_type in ["xlsx", "xls"]:
            df = pd.read_excel(file_path)
        elif file_type == "json":
            try:
                df = pd.read_json(file_path)
            except Exception:
                df = pd.read_json(file_path, lines=True)
        else:
            raise ValueError(f"Unsupported file format: {file_type}")

        # Ensure column names are clean strings
        df.columns = [str(col).strip() for col in df.columns]
        return df

    @staticmethod
    def load_to_duckdb(conn: duckdb.DuckDBPyConnection, table_name: str, df: pd.DataFrame):
        """Registers a pandas dataframe as a DuckDB table."""
        conn.register(table_name, df)
