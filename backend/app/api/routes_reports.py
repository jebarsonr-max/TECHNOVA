from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models import Analysis
from backend.app.reports.report_generator import ReportGenerator
from backend.app.schemas import AnalysisResponse

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/{id}")
def get_report(id: str, db: Session = Depends(get_db)):
    analysis = db.query(Analysis).filter(Analysis.id == id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    analysis_schema = AnalysisResponse.from_orm(analysis).dict()
    report = ReportGenerator.generate_report(analysis_schema)
    return report
