from pydantic import BaseModel, Field
from typing import List

class TechGap(BaseModel):
    skill: str = Field(description="Name of the missing or weak skill")
    risk_level: str = Field(description="High/Medium/Low risk for this specific role")
    learning_path: str = Field(description="Exactly what to learn (e.g., 'Learn RxJS for Angular state management')")

class ProjectOptimization(BaseModel):
    project_name: str = Field(description="Name of the candidate's project")
    current_stack: str = Field(description="Stack used in the project")
    architectural_advice: str = Field(description="How to re-engineer this project using JD's tech stack (e.g., migrating Node to Spring Boot)")

class SeniorDevFeedback(BaseModel):
    executive_summary: str = Field(description="A deep-dive (150-200 words) analysis of technical compatibility")
    technical_gaps: List[TechGap] = Field(description="A list of at least 5 deep technical gaps")
    project_deep_dive: List[ProjectOptimization] = Field(description="Specific advice to improve candidate's projects")
    interview_strategy: str = Field(description="How to handle questions about missing Java/Angular experience during the interview")