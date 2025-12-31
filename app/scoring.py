from app.extractors import extract_education,extract_skills,extract_contacts,extract_experience

def skill_score(extracted_data:dict)->int:
    skills = extracted_data.get("skills", [])
    return len(set(skills))

def education_score(extracted_data:dict)->int:
    degrees = extracted_data.get("education",{}).get("degrees",[])
    return len(set(degrees))

def contact_score(extracted_data:dict)->int:
    contacts = extracted_data.get("contacts",{})
    if contacts:
        return 1
    return 0

def experience_score(extracted_data:dict)->int:
    experience = extracted_data.get("experience",{})
    score = 0
    if len(experience.get("job_titles",[]))>=1:
        score += 1

    if len(experience.get("employment_keywords",[]))>=1:
        score += 1

    if len(experience.get("action_verbs",[]))>=2:
        score += 1

    if len(experience.get("metrics_pattern",[]))>=1:
        score += 1

    return score


