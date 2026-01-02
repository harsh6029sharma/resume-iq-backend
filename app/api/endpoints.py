from fastapi import APIRouter,UploadFile,File,Form,HTTPException
from app.utils import ats_match,extract_jd_skills
from app.services.resume_services import analyze_resume_bytes
from app.services.ai_feedback_service import generate_ai_feedback
from app.cleaning import newline,remove_extra_space,remove_special_chars,remove_emojis_and_icons
import json

router = APIRouter(prefix="/resume")

@router.post("/analysis")
async def resume_analysis(file:UploadFile=File(...), jd:str = Form(...))->dict:

    try:
        # Resume analysis
        pdf_bytes = await file.read()
        resume_result = analyze_resume_bytes(pdf_bytes,jd)

        resume_skills = resume_result["extracted_data"]["skills"]

        # JD skills extraction
        jd_skills = await extract_jd_skills(jd)

        #ATS matching
        ats_result = ats_match(resume_skills, jd_skills)

        return {
            "resume_skills": resume_skills,
            "jd_skills": jd_skills,
            "ats_result": ats_result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"ATS analysis failed: {str(e)}"
        )
    
@router.post("/feedback")
async def gen_ai_feedback(file:UploadFile=File(...), jd:str=Form(...)):
    
    try:
        # Resume analysis
        pdf_bytes = await file.read()
        resume_result = analyze_resume_bytes(pdf_bytes)
        resume_skills = resume_result["extracted_data"]["skills"]
        # JD skills extraction
        jd_text_wo_newline = newline(jd)
        jd_text_wo_extra_space = remove_extra_space(jd_text_wo_newline)
        jd_text_wo_special_char = remove_special_chars(jd_text_wo_extra_space)
        cleaned_jd = remove_emojis_and_icons(jd_text_wo_special_char)
        print(cleaned_jd)
        jd_skills = await extract_jd_skills(cleaned_jd)
        #ATS matching
        ats_result = ats_match(resume_skills, jd_skills)

        data = {
            "resume_skills": resume_skills,
            "jd_skills": jd_skills,
            "ats_result": ats_result
        }
        data_string = json.dumps(data)
        feedback = await generate_ai_feedback(data_string)
        print(f"This is feedback:{feedback}")
        return {"feedback":feedback}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"ATS analysis failed: {str(e)}"
        )