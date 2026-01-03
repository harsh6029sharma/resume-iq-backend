from fastapi import APIRouter,UploadFile,File,Form,HTTPException
from app.services.pipeline import extraction_pipeline
from app.utils.parsing import pdf_bytes_to_text
from app.utils.cleaning import clean_text
from app.services.scoring import calculate_ats_score
from app.schemas.resume import ATSResponse
from app.services.ai_service import get_llm_feedback

router = APIRouter(prefix="/resume")

@router.post("/analysis",response_model=ATSResponse)
async def resume_analysis(file:UploadFile=File(...), jd:str = Form(...)):
    try:
        # cleaning the raw text
        resume_pdf_bytes = await file.read()
        # raw text of resume
        raw_resume_text = pdf_bytes_to_text(resume_pdf_bytes)
        # normalizing data
        resume_clean_text = clean_text(raw_resume_text)
        # extracting data
        resume_all_data = extraction_pipeline(resume_clean_text)
        # first clean the jd 
        clean_jd_text = clean_text(jd)
        # extract skills from jd
        jd_all_data = extraction_pipeline(clean_jd_text)

        ats_results= calculate_ats_score(resume_all_data,jd_all_data)

        return ats_results
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"ATS analysis failed: {str(e)}"
        )
    

@router.post("/feedback")
async def ai_feedback(file:UploadFile=File(...), jd:str=Form(...)):
    
    try:
        resume_pdf_bytes = await file.read()
        # raw text of resume
        raw_resume_text = pdf_bytes_to_text(resume_pdf_bytes)
        # normalizing data
        resume_clean_text = clean_text(raw_resume_text)
        # extracting data
        resume_all_data = extraction_pipeline(resume_clean_text)
        # first clean the jd 
        clean_jd_text = clean_text(jd)
        # extract skills from jd
        jd_all_data = extraction_pipeline(clean_jd_text)

        ats_results= calculate_ats_score(resume_all_data,jd_all_data)

        result = await get_llm_feedback(ats_results,clean_jd_text,ats_results["overall_match"])

        return result
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"ATS analysis failed: {str(e)}"
        )