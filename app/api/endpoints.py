from fastapi import APIRouter,UploadFile,File,Form,HTTPException
from app.services.resume_services import process_resume_bytes,process_jd_text
from app.services.scoring import calculate_ats_score
from app.schemas.resume_schema import ATSResponse
from app.services.resume_services import create_analysis_flow
from app.db.config import sessionDep
from app.models.models import User
from fastapi import Depends
from app.dependencies.account_dependencies import get_current_user

router = APIRouter(prefix="/resume", tags=["Resume"])

@router.post("/analysis",response_model=ATSResponse)
async def resume_analysis(file:UploadFile=File(...), jd:str = Form(...), current_user:User=Depends(get_current_user)):
    try:
        # cleaning the raw text
        resume_pdf_bytes = await file.read()
        resume_all_data = process_resume_bytes(resume_pdf_bytes)
        jd_all_data = process_jd_text(jd)
        ats_results= calculate_ats_score(resume_all_data,jd_all_data)
        return {
            "current_user":current_user,
            "ats_results":ats_results
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"ATS analysis failed: {str(e)}"
        )


@router.post("/feedback")
async def ai_feedback(session:sessionDep,file:UploadFile=File(...), jd:str=Form(...), current_user:User = Depends(get_current_user)):
    try:
        resume_pdf_bytes = await file.read()
        resume_all_data = process_resume_bytes(resume_pdf_bytes)
        jd_all_data = process_jd_text(jd)
        ats_results= calculate_ats_score(resume_all_data,jd_all_data)
        base_score = ats_results.get("overall_match") or ats_results.get("score") or 0
        analysis_record = await create_analysis_flow(
            session=session,
            pdf_bytes = resume_pdf_bytes,
            jd_text = jd,
            base_score = base_score,
            current_user=current_user
        )
        return {
            "status":"success",
            "analysis_id":analysis_record.id,
            "feedback":analysis_record.full_feedback
        }


    except Exception as e:
        # just for debugging
        import traceback
        print(f"Full Error Traceback:\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"AI Feedback failed: {str(e)}"
        )