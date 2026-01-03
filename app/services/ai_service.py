from langchain_groq import ChatGroq
# from langchain_openai import ChatOpenAI
from fastapi import HTTPException
from langchain_core.output_parsers import PydanticOutputParser
from app.schemas.ai_schema import SeniorDevFeedback
from app.prompts.analysis_prompt import prompt
import os
from dotenv import load_dotenv

load_dotenv()

parser = PydanticOutputParser(pydantic_object=SeniorDevFeedback)

llm = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

# llm = ChatOpenAI(
#     model="gpt-5-nano",
#     api_key=os.getenv("OPENAI_API_KEY")
    
# )

async def get_llm_feedback(resume_data,jd_text,base_score):
    try:
        formatted_prompt = prompt.format(
            resume_data=resume_data,
            jd_text=jd_text,
            base_score=base_score,
            format_instructions=parser.get_format_instructions()
        )
        response = await llm.ainvoke(formatted_prompt)
        return parser.parse(response.content)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI feedback failed:{str(e)}"
        )
 