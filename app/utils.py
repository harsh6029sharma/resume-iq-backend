from app.extractors import extract_skills
from app.services.llm_service import extract_jd_skills_from_llm


def score_label(overall_score:int)->str:
    if overall_score >= 8:
        return "strong"
    elif overall_score>=5:
        return "medium"
    else:
        return "weak"


def ats_match(resume_skills: list, jd_skills: list) -> dict:
    resume_set = set(resume_skills)
    jd_set = set(jd_skills)

    matched = resume_set & jd_set
    missing = jd_set - resume_set

    match_percentage = round(
        (len(matched) / len(jd_set)) * 100, 2
    ) if jd_set else 0

    return {
        "match_percentage": match_percentage,
        "matched_skills": list(matched),
        "missing_skills": list(missing)
    }

async def extract_jd_skills(jd_text:str)->list:
    jd_text=jd_text.lower()
    jd_skills = await extract_jd_skills_from_llm(jd_text)
    return jd_skills
