from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.app.database import get_db
from backend.app.models import Analysis, Proof, Evidence
from backend.app.schemas import ProofSchema, EvidenceSchema

router = APIRouter(prefix="/analysis", tags=["Proof & Evidence"])

@router.get("/{id}/proof", response_model=ProofSchema)
def get_analysis_proof(id: str, db: Session = Depends(get_db)):
    analysis = db.query(Analysis).filter(Analysis.id == id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    if not analysis.proof:
        raise HTTPException(status_code=404, detail="Proof not generated for this analysis")

    return analysis.proof

@router.get("/{id}/evidence", response_model=List[EvidenceSchema])
def get_analysis_evidence(id: str, db: Session = Depends(get_db)):
    analysis = db.query(Analysis).filter(Analysis.id == id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    if not analysis.proof or not analysis.proof.evidence_items:
        return []

    return analysis.proof.evidence_items
