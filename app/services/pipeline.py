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

def scoring_pipeline(extracted_data: dict, jd_data: dict) -> dict:x