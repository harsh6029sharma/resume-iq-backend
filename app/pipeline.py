from app.cleaning import remove_emojis_and_icons,remove_extra_space,newline,remove_special_chars
from app.parsing import pdf_bytes_to_text
from app.extractors import extract_education,extract_skills,extract_contacts,extract_experience
from app.scoring import skill_score,experience_score,education_score,contact_score
import re

def cleaning_pipeline(pdf_bytes:bytes)->str: 
    pdf_text = pdf_bytes_to_text(pdf_bytes)
    pdf_text_wo_emojis_icons = remove_emojis_and_icons(pdf_text)
    pdf_text_no_emoji = remove_special_chars(pdf_text_wo_emojis_icons)
    pdf_text_without_newline = newline(pdf_text_no_emoji)
    clean_pdf_text = remove_extra_space(pdf_text_without_newline)
    return clean_pdf_text


def extraction_pipeline(text:str)->dict:
    skills = extract_skills(text)
    education = extract_education(text)
    contacts = extract_contacts(text)
    experience = extract_experience(text)
    return {
        "skills":skills,
        "education":education,
        "contacts":contacts,
        "experience":experience
    }

def scoring_pipeline(extracted_data:dict)->int:
    skills_score = skill_score(extracted_data)
    educations_score = education_score(extracted_data)
    experiences_score = experience_score(extracted_data)
    contacts_score = contact_score(extracted_data)
    raw_score = (
        skills_score +
        educations_score +
        experiences_score +
        contacts_score
    )
    # overall score is in range of 0-10
    MAX_SCORE = 11  # defined max
    normalized_score = round((raw_score / MAX_SCORE) * 10)

    return normalized_score