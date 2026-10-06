import uuid
from typing import Dict, Any, List
from sqlalchemy.orm import Session

from backend.app.models import Analysis, AnalysisStep, Proof, ExecutionResult, VerificationResult, Evidence, Dataset
from backend.app.agents.question_analyzer import QuestionAnalyzer
from backend.app.agents.planner import AnalysisPlanner
from backend.app.agents.code_agent import CodeAgent
from backend.app.agents.repair_agent import RepairAgent
from backend.app.execution.executor import SecureCodeExecutor
from backend.app.verification.verifier import VerificationEngine
from backend.app.verification.evidence import EvidenceBuilder
from backend.app.data.schema import DatasetSchemaExtractor

class AgentWorkflowStateMachine:
    @staticmethod
    def run_analysis_pipeline(db: Session, analysis_id: str) -> Analysis:
        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
        if not analysis:
            raise ValueError(f"Analysis record {analysis_id} not found.")

        analysis.status = "IN_PROGRESS"
        db.commit()

        # Step 1: Fetch Datasets metadata
        datasets = db.query(Dataset).filter(Dataset.id.in_(analysis.dataset_ids)).all()
        datasets_schema = []
        datasets_meta = []
        for ds in datasets:
            cols_meta = [c.__dict__ for c in ds.columns]
            ds_dict = ds.__dict__
            schema = DatasetSchemaExtractor.extract_schema_summary(ds_dict, cols_meta)
            datasets_schema.append(schema)
            
            datasets_meta.append({
                "dataset_id": ds.id,
                "original_filename": ds.original_filename,
                "file_path": ds.file_path,
                "file_type": ds.file_type,
                "row_count": ds.row_count,
                "columns": cols_meta,
                "quality_report": ds.quality_report or {}
            })

        # Step 2: Question Understanding
        step1 = AnalysisStep(
            id=str(uuid.uuid4()),
            analysis_id=analysis_id,
            step_number=1,
            title="Question Understanding & Trap Inspection",
            description="Inspecting schema, detecting column intents, and checking PS08 adversarial traps.",
            status="IN_PROGRESS"
        )
        db.add(step1)
        db.commit()

        interpreted = QuestionAnalyzer.analyze_question(analysis.question, datasets_schema)
        analysis.intent = interpreted.get("intent")
        analysis.interpreted_question = interpreted
        step1.status = "COMPLETED"
        db.commit()

        # Step 3: Analysis Planning
        step2 = AnalysisStep(
            id=str(uuid.uuid4()),
            analysis_id=analysis_id,
            step_number=2,
            title="Analysis Planning",
            description="Formulating step-by-step calculation plan or refusal logic.",
            status="IN_PROGRESS"
        )
        db.add(step2)
        db.commit()

        plan = AnalysisPlanner.create_plan(interpreted, datasets_schema)
        analysis.plan_steps = plan.get("steps")
        step2.status = "COMPLETED"
        db.commit()

        # Handle Refusal Case
        if plan.get("is_refusal"):
            refusal_reason = plan.get("refusal_reason")
            analysis.status = "CANNOT_DETERMINE"
            analysis.verification_status = "CANNOT_DETERMINE"
            analysis.verification_score = 0.0
            analysis.final_answer = f"CANNOT_DETERMINE: {refusal_reason}"
            analysis.refusal_reason = refusal_reason

            proof_code_obj = CodeAgent.generate_proof_code(analysis.question, plan, datasets_meta)
            proof = Proof(
                id=str(uuid.uuid4()),
                analysis_id=analysis_id,
                generated_code=proof_code_obj["code"],
                code_language="python",
                execution_status="REFUSED",
                verification_status="CANNOT_DETERMINE",
                verification_score=0.0,
                calculation_explanation=refusal_reason,
                assumptions=["No guess rule enforced for insufficient/ambiguous data."]
            )
            db.add(proof)
            db.commit()
            return analysis

        # Step 4: Code Generation
        step3 = AnalysisStep(
            id=str(uuid.uuid4()),
            analysis_id=analysis_id,
            step_number=3,
            title="Proof Code Generation",
            description="Generating deterministic Python proof code targeting actual dataset columns.",
            status="IN_PROGRESS"
        )
        db.add(step3)
        db.commit()

        code_obj = CodeAgent.generate_proof_code(analysis.question, plan, datasets_meta)
        proof_code = code_obj["code"]
        step3.status = "COMPLETED"
        db.commit()

        # Step 5: Secure Execution & Repair Loop (Up to 3 Attempts)
        step4 = AnalysisStep(
            id=str(uuid.uuid4()),
            analysis_id=analysis_id,
            step_number=4,
            title="Secure Sandbox Execution",
            description="Executing proof code inside isolated sandbox with timeout and memory limits.",
            status="IN_PROGRESS"
        )
        db.add(step4)
        db.commit()

        exec_res = SecureCodeExecutor.execute_code(proof_code)
        repair_attempts = 0
        repair_history = []

        while not exec_res.get("is_success") and repair_attempts < 3:
            repair_attempts += 1
            err_msg = exec_res.get("stderr", "Unknown error")
            repair_info = RepairAgent.repair_code(analysis.question, proof_code, err_msg, repair_attempts)
            proof_code = repair_info["repaired_code"]
            repair_history.append(repair_info)
            exec_res = SecureCodeExecutor.execute_code(proof_code)

        step4.status = "COMPLETED" if exec_res.get("is_success") else "FAILED"
        db.commit()

        # Step 6: Verification Engine
        step5 = AnalysisStep(
            id=str(uuid.uuid4()),
            analysis_id=analysis_id,
            step_number=5,
            title="Verification & Independent Cross-Check",
            description="Cross-checking numerical result using DuckDB and verifying math/unit consistency.",
            status="IN_PROGRESS"
        )
        db.add(step5)
        db.commit()

        quality_report = datasets_meta[0].get("quality_report", {}) if datasets_meta else {}
        ver_info = VerificationEngine.verify(exec_res, proof_code, datasets_meta, quality_report)
        step5.status = "COMPLETED"
        db.commit()

        # Step 7: Build Evidence & Finalize Proof
        step6 = AnalysisStep(
            id=str(uuid.uuid4()),
            analysis_id=analysis_id,
            step_number=6,
            title="Evidence & Answer Packaging",
            description="Packaging executable proof card, evidence items, and final answer.",
            status="IN_PROGRESS"
        )
        db.add(step6)
        db.commit()

        evidence_data = EvidenceBuilder.build_evidence(exec_res, ver_info, datasets_meta)

        # Create Proof DB Record
        proof = Proof(
            id=str(uuid.uuid4()),
            analysis_id=analysis_id,
            generated_code=proof_code,
            code_language="python",
            execution_status="SUCCESS" if exec_res.get("is_success") else "FAILED",
            verification_status=ver_info["verification_status"],
            verification_score=ver_info["verification_score"],
            source_datasets=[ds.get("original_filename") for ds in datasets_meta],
            relevant_columns=interpreted.get("required_columns", []),
            filters_applied=interpreted.get("filters", []),
            transformations=["Loaded pandas DataFrame", "Cleaned missing values", "Calculated target metric"],
            calculation_explanation=f"Executed analytical script to calculate {interpreted.get('metric', 'value')} across target columns.",
            assumptions=["Data quality check verified source integrity."]
        )
        db.add(proof)
        db.flush()

        # Execution Result DB Record
        exec_db = ExecutionResult(
            id=str(uuid.uuid4()),
            proof_id=proof.id,
            exit_code=exec_res.get("exit_code", 0),
            stdout=exec_res.get("stdout"),
            stderr=exec_res.get("stderr"),
            execution_time_ms=exec_res.get("execution_time_ms", 0.0),
            result_data=exec_res.get("result_data"),
            is_success=exec_res.get("is_success", False),
            repair_attempts=repair_attempts,
            repair_history=repair_history
        )
        db.add(exec_db)

        # Verification Result DB Record
        ver_db = VerificationResult(
            id=str(uuid.uuid4()),
            proof_id=proof.id,
            reproducibility_passed=ver_info["reproducibility_passed"],
            independent_check_passed=ver_info["independent_check_passed"],
            math_check_passed=ver_info["math_check_passed"],
            unit_check_passed=ver_info["unit_check_passed"],
            data_quality_check_passed=ver_info["data_quality_check_passed"],
            primary_method_result=ver_info["primary_method_result"],
            independent_method_result=ver_info["independent_method_result"],
            verification_notes=ver_info["notes"]
        )
        db.add(ver_db)

        # Evidence DB Records
        for ev in evidence_data:
            ev_db = Evidence(
                id=str(uuid.uuid4()),
                proof_id=proof.id,
                evidence_type=ev["evidence_type"],
                title=ev["title"],
                content=ev["content"]
            )
            db.add(ev_db)

        # Set final answer
        result_val = exec_res.get("result_data", {}).get("answer") if exec_res.get("result_data") else None
        if result_val is not None:
            analysis.final_answer = str(result_val)
        else:
            analysis.final_answer = "CANNOT_DETERMINE: Execution failed or produced non-numerical output."
            analysis.verification_status = "CANNOT_DETERMINE"

        analysis.status = "COMPLETED"
        analysis.verification_status = ver_info["verification_status"]
        analysis.verification_score = ver_info["verification_score"]
        step6.status = "COMPLETED"

        db.commit()
        db.refresh(analysis)
        return analysis
