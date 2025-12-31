def ats_match_service(resume_skills, jd_skills):
    resume_set = set(resume_skills)
    jd_set = set(jd_skills)

    matched = resume_set & jd_set
    missing = jd_set - resume_set

    percentage = round((len(matched) / len(jd_set)) * 100) if jd_set else 0

    return {
        "match_percentage": percentage,
        "matched_skills": list(matched),
        "missing_skills": list(missing)
    }
