from langchain_groq import ChatGroq
from fastapi import HTTPException
from langchain_core.output_parsers import PydanticOutputParser
from app.schemas.ai_schema import SeniorDevFeedback
from app.prompts.analysis_prompt import prompt_template
import os
from dotenv import load_dotenv

load_dotenv()

parser = PydanticOutputParser(pydantic_object=SeniorDevFeedback)

llm = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

async def get_llm_feedback(resume_data,jd_text,base_score):
    try:
        formatted_prompt = prompt_template.format(
            resume_data=resume_data,
            jd_text=jd_text,
            base_score=base_score,
            format_instructions=parser.get_format_instructions()
        )
        response = await llm.ainvoke(formatted_prompt)
        parsed_feedback = parser.parse(response.content)
        return parsed_feedback
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI feedback failed:{str(e)}"
        )
 