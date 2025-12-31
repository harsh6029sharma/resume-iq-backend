from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
import json
import re

load_dotenv()

def get_llm():
    return ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="qwen/qwen3-32b",
        temperature=0,
    )

async def generate_ai_feedback(data:str):
    system_prompt = """
        Rules:
        - Do NOT include <think>
        - Do NOT include reasoning
        - Do NOT include explanations
        - Return ONLY valid JSON
        - Output must start with { and end with }

            You are an experienced technical recruiter and ATS (Applicant Tracking System) expert.

        Your task is to analyze a resume against the given job description skills and the ATS matching result, and then provide honest, realistic, and actionable feedback to improve the resume.

        Here is the data:

        Resume Skills:
        {{resume_skills}}

        Job Description Skills:
        {{jd_skills}}

        ATS Result:
        {{ats_result}}

        Analyze the alignment between resume skills and job description skills.
        Check whether the ATS match percentage is logically correct or inflated.
        Evaluate the resume from both an automated ATS system and a human recruiter perspective.

        Now provide feedback in the following structured format:

        1. Overall Match Assessment
        - Is the ATS match percentage realistic?
        - Would a real ATS or recruiter shortlist this resume?

        2. Strengths
        - Skills that clearly match the job description
        - Strong signals from the resume

        3. Missing or Weak Skills
        - Skills required in the JD but missing or weak in the resume
        - Mention if any critical or deal-breaker skills are absent

        4. Resume Improvement Suggestions
        - How to improve or rephrase skills for better ATS matching
        - Suggestions for adding projects, tools, or keywords
        - Tips to make the resume more role-specific

        5. ATS Optimization Tips
        - Keyword usage and placement suggestions
        - Skill phrasing improvements
        - Formatting or section-level advice

        6. Final Verdict
        - Shortlisting probability (Low / Medium / High)
        - One-line recruiter verdict

        Do NOT include <think> or reasoning.


    """
    llm = get_llm()

    messages = [
        ("system", system_prompt),
        ("human", data),
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
    print(json_str)
    
    try:
        # convert raw output into a dictionary 
        data = json.loads(json_str)
        # print(data)
        return data
    
    except Exception as e:
        print("JD SKILL PARSE ERROR:", str(e))
        return {}
