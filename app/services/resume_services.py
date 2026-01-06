from app.services.pipeline import extraction_pipeline
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Job
from app.dependencies.account_dependencies import get_current_user
from app.models.models import User,Candidate,Analysis
from fastapi import Depends
from app.services.ai_service import get_llm_feedback
from app.utils.parsing import pdf_bytes_to_text
from app.utils.cleaning import clean_text

# parsing
def process_resume_bytes(resume_pdf_bytes:bytes):
    # extracting raw resume text
    raw_resume_text = pdf_bytes_to_text(resume_pdf_bytes)
    # normalizing data

    resume_clean_text = clean_text(raw_resume_text)
    # extracting data
    resume_all_data = extraction_pipeline(resume_clean_text)
    return resume_all_data


def process_jd_text(jd:str):
    # first clean the jd 
    clean_jd_text = clean_text(jd)
    # extract skills from jd
    jd_all_data = extraction_pipeline(clean_jd_text)

    return jd_all_data


# to save the analysis of resume
async def create_analysis_flow(session:AsyncSession,pdf_bytes:bytes,jd_text:str,base_score:float, current_user:User):

    try:
        resume_data = process_resume_bytes(pdf_bytes)
        ai_feedback = await get_llm_feedback(
            resume_data=resume_data,
            jd_text=jd_text,
            base_score=base_score
        )

        # first save job description
        new_job = Job(
            user_id = current_user.id,
            job_title = ai_feedback.job_title,
            description = jd_text
        )
        session.add(new_job)
        await session.flush()

        # now save candidate
        new_candidate = Candidate(
            user_id = current_user.id,
            name=ai_feedback.candidate_name,
            resume_text = str(resume_data)
        )

        session.add(new_candidate)
        await session.flush()

        # now save analysis
        new_analysis = Analysis(
            user_id = current_user.id,
            job_id = new_job.id,
            candidate_id = new_candidate.id,
            score = base_score,
            full_feedback = ai_feedback.model_dump() # converts pydantic into json
        )
        session.add(new_analysis)
        await session.commit()
        await session.refresh(new_analysis)
        return new_analysis

    except Exception as e:
        await session.rollback()
        raise e
