from pydantic import BaseModel
from typing import Optional,Dict,List
from app.schemas.ai_schema import SeniorDevFeedback

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

class AnalysisBase(BaseModel):
    score:float
    job_id:int
    candidate_id:int

class AnalysisCreate(AnalysisBase):
    full_feedback:SeniorDevFeedback

class AnalysisResponse(BaseModel):
    id:int
    user_id:int
    job_id:int
    candidate_id:int