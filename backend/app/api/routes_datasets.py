import os
import uuid
import shutil
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict

from backend.app.database import get_db
from backend.app.models import Dataset, DatasetColumn
from backend.app.schemas import DatasetSchema, RelationshipSchema
from backend.app.data.ingestion import DataIngestionEngine
from backend.app.data.profiler import DataProfiler
from backend.app.data.quality import QualityChecker
from backend.app.data.relationships import RelationshipDetector

router = APIRouter(prefix="/datasets", tags=["Datasets"])

UPLOAD_DIR = os.path.abspath("./data/uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=DatasetSchema)
def upload_dataset(file: UploadFile = File(...), db: Session = Depends(get_db)):
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower().strip(".")
    if ext not in ["csv", "xlsx", "xls", "json"]:
        raise HTTPException(status_code=400, detail=f"Unsupported file extension '{ext}'. Only CSV, XLSX, and JSON are supported.")

    dataset_id = str(uuid.uuid4())
    saved_filename = f"{dataset_id}_{filename}"
    saved_filepath = os.path.join(UPLOAD_DIR, saved_filename)

    with open(saved_filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_size = os.path.getsize(saved_filepath)

    try:
        # Load and Profile
        df = DataIngestionEngine.load_dataset(saved_filepath, ext)
        profile_res = DataProfiler.profile(df)
        quality_res = QualityChecker.generate_quality_report(profile_res)

        dataset_rec = Dataset(
            id=dataset_id,
            filename=saved_filename,
            original_filename=filename,
            file_type=ext,
            file_size_bytes=file_size,
            file_path=saved_filepath,
            row_count=profile_res["row_count"],
            column_count=profile_res["column_count"],
            profiling_summary=profile_res,
            quality_report=quality_res
        )
        db.add(dataset_rec)

        for col_info in profile_res["columns"]:
            col_rec = DatasetColumn(
                id=str(uuid.uuid4()),
                dataset_id=dataset_id,
                name=col_info["name"],
                data_type=col_info["data_type"],
                detected_type=col_info["detected_type"],
                missing_count=col_info["missing_count"],
                unique_count=col_info["unique_count"],
                min_value=col_info.get("min_value"),
                max_value=col_info.get("max_value"),
                mean_value=col_info.get("mean_value"),
                currency_symbol=col_info.get("currency_symbol"),
                detected_unit=col_info.get("detected_unit"),
                is_identifier=col_info.get("is_identifier", False),
                suspicious_values=col_info.get("suspicious_values")
            )
            db.add(col_rec)

        db.commit()
        db.refresh(dataset_rec)
        return dataset_rec

    except Exception as e:
        if os.path.exists(saved_filepath):
            os.remove(saved_filepath)
        raise HTTPException(status_code=500, detail=f"Failed to ingest and profile dataset: {str(e)}")

@router.get("", response_model=List[DatasetSchema])
def list_datasets(db: Session = Depends(get_db)):
    return db.query(Dataset).order_by(Dataset.created_at.desc()).all()

@router.get("/relationships", response_model=List[RelationshipSchema])
def get_dataset_relationships(db: Session = Depends(get_db)):
    datasets = db.query(Dataset).all()
    if len(datasets) < 2:
        return []

    dataframes = {}
    ds_dicts = []
    for ds in datasets:
        try:
            df = DataIngestionEngine.load_dataset(ds.file_path, ds.file_type)
            dataframes[ds.id] = df
            ds_dicts.append({"id": ds.id, "name": ds.original_filename})
        except Exception:
            pass

    return RelationshipDetector.detect_relationships(ds_dicts, dataframes)

@router.get("/{id}", response_model=DatasetSchema)
def get_dataset(id: str, db: Session = Depends(get_db)):
    dataset = db.query(Dataset).filter(Dataset.id == id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return dataset

@router.delete("/{id}")
def delete_dataset(id: str, db: Session = Depends(get_db)):
    dataset = db.query(Dataset).filter(Dataset.id == id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    if os.path.exists(dataset.file_path):
        try:
            os.remove(dataset.file_path)
        except Exception:
            pass

    db.delete(dataset)
    db.commit()
    return {"message": "Dataset deleted successfully", "id": id}
