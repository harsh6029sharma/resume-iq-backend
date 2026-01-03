from pydantic import BaseModel
from typing import Optional,Dict,List

class ScoreBreakdown(BaseModel):
    skill_score: float
    experience_score: float
    education_score: float

class ATSResponse(BaseModel):
    overall_match: float
    breakdown: ScoreBreakdown
    matched_skills: List[str]
    missing_skills: List[str]
    impact_level: str
    extracted_resume: Optional[Dict] = None