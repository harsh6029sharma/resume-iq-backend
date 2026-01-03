from app.extractors.extractor import extract_education,extract_skills,extract_experience,extract_contact

def extraction_pipeline(text:str):
    skills = extract_skills(text)
    education = extract_education(text)
    contacts = extract_contact(text)
    experience = extract_experience(text)
    return {
        "skills":skills,
        "education":education,
        "contacts":contacts,
        "experience":experience
    }