from fastapi import FastAPI,UploadFile,File,HTTPException,Form
from app.utils import ats_match,extract_jd_skills
from app.services.resume_services import analyze_resume_bytes
from app.services.ai_feedback_service import generate_ai_feedback
import json

app = FastAPI()

@app.post("/analyze-resume")
async def analyze_resume(file:UploadFile=File(...))->dict:
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="only pdf files allowed")
    
    try:
        pdf_bytes = await file.read()
        overall_data = analyze_resume_bytes(pdf_bytes)
        return overall_data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"resume processing failed:{str(e)}")


@app.post("/ats-analysis")
async def ats_analysis(file:UploadFile=File(...), jd:str = Form(...))->dict:

    # if not file.filename.startswith(".pdf"):
    #     raise HTTPException(status_code=400,detail="only pdf allowed")
    
    try:
        # Resume analysis
        pdf_bytes = await file.read()
        resume_result = analyze_resume_bytes(pdf_bytes)

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
    

@app.post("/ai-feedback")
async def gen_ai_feedback(file:UploadFile=File(...), jd:str=Form(...)):

    # if not file.filename.startswith(".pdf"):
    #     raise HTTPException(status_code=400,detail="only pdf allowed")
    
    try:
        # Resume analysis
        pdf_bytes = await file.read()
        resume_result = analyze_resume_bytes(pdf_bytes)
        resume_skills = resume_result["extracted_data"]["skills"]
        # JD skills extraction
        jd_skills = await extract_jd_skills(jd)
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