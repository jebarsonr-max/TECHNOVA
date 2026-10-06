import uuid
import os
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.app.database import get_db
from backend.app.models import Analysis
from backend.app.schemas import QuestionRequest, AnalysisResponse
from backend.app.workflow.state_machine import AgentWorkflowStateMachine

router = APIRouter(prefix="/analysis", tags=["Analysis"])

@router.post("", response_model=AnalysisResponse)
def create_analysis(req: QuestionRequest, db: Session = Depends(get_db)):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    if not req.dataset_ids:
        raise HTTPException(status_code=400, detail="At least one dataset_id must be provided.")

    analysis_id = str(uuid.uuid4())
    analysis = Analysis(
        id=analysis_id,
        question=req.question,
        dataset_ids=req.dataset_ids,
        status="PENDING",
        verification_status="UNVERIFIED",
        verification_score=0.0
    )
    db.add(analysis)
    db.commit()

    # Execute state machine pipeline synchronously for reliable demo execution
    completed_analysis = AgentWorkflowStateMachine.run_analysis_pipeline(db, analysis_id)
    return completed_analysis

@router.get("/history", response_model=List[AnalysisResponse])
def get_analysis_history(db: Session = Depends(get_db)):
    return db.query(Analysis).order_by(Analysis.created_at.desc()).all()

@router.get("/{id}", response_model=AnalysisResponse)
def get_analysis(id: str, db: Session = Depends(get_db)):
    analysis = db.query(Analysis).filter(Analysis.id == id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis

demo_router = APIRouter(prefix="/demo", tags=["Demo"])

@demo_router.get("/questions")
def get_demo_questions():
    demo_file = os.path.abspath("./data/demo/demo_questions.json")
    if os.path.exists(demo_file):
        with open(demo_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []
