def calculate_ats_score(resume_data, jd_data):
    # here we defined weights for each sections
    SKILL_WEIGHT = 0.60      # Skills are most important
    EXP_WEIGHT = 0.30        # Experience/Impact
    EDU_WEIGHT = 0.10        # Education

    # finding mathcing and missing skills 
    # skill score calculation
    r_skills = set(resume_data.get("skills",[]))
    j_skills = set(jd_data.get("skills",[]))

    
    if not j_skills:
        skill_score = 0
        matched_skills = []
        missing_skills = []
    else:
        matched_skills = list(r_skills.intersection(j_skills))
        missing_skills = list(j_skills-r_skills)
        skill_score = (len(matched_skills)/len(j_skills))*100

    # Experience/impact score 
    # score on the basis of metrics and action verbs 
    metrics_count = resume_data.get("experience", {}).get("total_impact_count", 0)
    verb_count = len(resume_data.get("experience", {}).get("action_verbs", []))
     
    exp_score = min((metrics_count * 15) + (verb_count * 5), 100)

   # Education Logic
    edu_match = 0
    jd_degrees = set(jd_data.get("education", {}).get("degrees", []))
    res_degrees = set(resume_data.get("education", {}).get("degrees", []))

    if not jd_degrees:
        edu_match = 100
    elif jd_degrees.intersection(res_degrees):
        edu_match = 100
    else:
        edu_match = 0

    # 4. FINAL WEIGHTED SCORE
    final_score = (skill_score * SKILL_WEIGHT) + (exp_score * EXP_WEIGHT) + (edu_match * EDU_WEIGHT)

    return {
        "overall_match": round(final_score, 2),
        "breakdown": {
            "skill_score": round(skill_score, 2),
            "experience_score": round(exp_score, 2),
            "education_score": edu_match
        },
        "analysis": {
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "impact_level": "High" if (metrics_count>2 and skill_score>60 ) else ("Medium" if metrics_count>0 else "Low")
        }
    }