import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import re
import json
load_dotenv()


def get_llm():
    return ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="qwen/qwen3-32b",
        temperature=0,
    )


async def extract_jd_skills_from_llm(jd_text:str)->list:
    
    if not jd_text or len(jd_text.strip()) < 20:
        return []
    
    system_prompt = """
        You are an ATS system.

            RULES (VERY IMPORTANT):
            - Do NOT explain anything
            - Do NOT include reasoning
            - Do NOT include <think> or analysis
            - Output ONLY valid JSON
            - No text before or after JSON

            Return JSON exactly in this format:
            {
            "skills": ["python", "docker", "aws"]
            }
        """
    
    llm = get_llm()


    messages = [
        ("system", system_prompt),
        ("human", jd_text),
    ]

    # async llm call
    response = await llm.ainvoke(messages)
    # raw output is a string response from llm
    raw_output = response.content.strip()

    # Extract JSON block safely
    match = re.search(r"\{[\s\S]*\}", raw_output)

    if not match:
        print("No JSON found in LLM output")
        return []

    json_str = match.group(0)

    

    try:
        # convert raw output into a dictionary 
        data = json.loads(json_str)
        skills = data.get("skills", [])
        return list(set(skill.lower().strip() for skill in skills))
    except Exception as e:
        print("JD SKILL PARSE ERROR:", str(e))
        return []
