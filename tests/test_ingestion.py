import os
import pytest
from backend.app.data.ingestion import DataIngestionEngine
from backend.app.data.profiler import DataProfiler

def test_csv_ingestion_and_profiling():
    csv_path = os.path.abspath("./data/demo/orders.csv")
    assert os.path.exists(csv_path)

    df = DataIngestionEngine.load_dataset(csv_path, "csv")
    assert len(df) == 8
    assert "total_amount" in df.columns

    profile = DataProfiler.profile(df)
    assert profile["row_count"] == 8
    assert profile["column_count"] == 6
    assert "total_amount" in profile["numeric_columns"]
