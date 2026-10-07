import os
import zipfile
import pandas as pd
import duckdb
from typing import Tuple, Dict, Any

MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024  # 50 MB limit

class DataIngestionEngine:
    @staticmethod
    def load_dataset(file_path: str, file_type: str) -> pd.DataFrame:
        """
        Loads CSV, XLSX, XLS, or JSON into a pandas DataFrame cleanly while leaving the source file untouched (immutable).
        Handles multi-sheet Excel files, multiple encodings, empty worksheets, corrupted files, and blank rows.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Dataset file not found at {file_path}")

        file_size = os.path.getsize(file_path)
        if file_size == 0:
            raise ValueError("The uploaded file is completely empty (0 bytes).")
        if file_size > MAX_FILE_SIZE_BYTES:
            raise ValueError(f"File size exceeds the maximum limit of 50 MB ({round(file_size / (1024 * 1024), 2)} MB).")

        file_type = file_type.lower().strip(".")

        df = None

        if file_type == "csv":
            df = DataIngestionEngine._load_csv(file_path)
        elif file_type in ["xlsx", "xls"]:
            df = DataIngestionEngine._load_excel(file_path, file_type)
        elif file_type == "json":
            df = DataIngestionEngine._load_json(file_path)
        else:
            raise ValueError(f"Unsupported file format '.{file_type}'. Supported formats are .csv, .xlsx, .xls, and .json.")

        if df is None or df.empty or len(df.columns) == 0:
            raise ValueError("The uploaded dataset contains no valid data rows or columns.")

        # Clean up column names & blank rows
        df = DataIngestionEngine._clean_dataframe(df)

        return df

    @staticmethod
    def _load_csv(file_path: str) -> pd.DataFrame:
        encodings = ["utf-8", "utf-8-sig", "latin1", "cp1252", "iso-8859-1"]
        last_exception = None

        for encoding in encodings:
            try:
                df = pd.read_csv(file_path, encoding=encoding, skip_blank_lines=True)
                return df
            except pd.errors.EmptyDataError:
                raise ValueError("The uploaded CSV file is empty or contains no readable columns.")
            except Exception as e:
                last_exception = e

        for encoding in encodings:
            try:
                df = pd.read_csv(file_path, encoding=encoding, sep=None, engine='python', skip_blank_lines=True, on_bad_lines='skip')
                return df
            except Exception as e:
                last_exception = e

        raise ValueError(f"Failed to parse CSV file: {str(last_exception)}")

    @staticmethod
    def _load_excel(file_path: str, file_type: str) -> pd.DataFrame:
        try:
            excel_file = pd.ExcelFile(file_path)
        except zipfile.BadZipFile:
            raise ValueError("Corrupted or invalid Excel (.xlsx) file structure.")
        except Exception as e:
            err_msg = str(e).lower()
            if "password" in err_msg or "encrypted" in err_msg:
                raise ValueError("Password-protected Excel files are not supported. Please unprotect the file before uploading.")
            raise ValueError(f"Failed to open Excel file: {str(e)}")

        sheet_names = excel_file.sheet_names
        if not sheet_names:
            raise ValueError("The Excel workbook contains no worksheets.")

        for sheet in sheet_names:
            try:
                df = excel_file.parse(sheet_name=sheet)
                df = df.dropna(how='all')
                if not df.empty and len(df.columns) > 0:
                    return df
            except Exception:
                continue

        raise ValueError("All worksheets in the Excel file are empty or contain no valid data.")

    @staticmethod
    def _load_json(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_json(file_path)
        except Exception:
            try:
                return pd.read_json(file_path, lines=True)
            except Exception as e:
                raise ValueError(f"Failed to parse JSON file: {str(e)}")

    @staticmethod
    def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        df = df.dropna(how='all')
        df = df.dropna(axis=1, how='all')

        if df.empty:
            raise ValueError("Dataset has no non-empty rows.")

        clean_cols = []
        seen_cols = {}
        for idx, col in enumerate(df.columns):
            col_str = str(col).strip()
            if not col_str or col_str.startswith("Unnamed:"):
                col_str = f"Column_{idx + 1}"
            
            if col_str in seen_cols:
                seen_cols[col_str] += 1
                col_str = f"{col_str}_{seen_cols[col_str]}"
            else:
                seen_cols[col_str] = 0

            clean_cols.append(col_str)

        df.columns = clean_cols
        return df

    @staticmethod
    def load_to_duckdb(conn: duckdb.DuckDBPyConnection, table_name: str, df: pd.DataFrame):
        """Registers a pandas dataframe as a DuckDB table."""
        conn.register(table_name, df)
