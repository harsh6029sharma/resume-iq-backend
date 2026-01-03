# keyword extraction
import re
from app.core.taxonomy import SKILLS_TAXONOMY,EDUCATION_TAXONOMY,CONTACT_PATTERNS,EXPERIENCE_TAXONOMY
from thefuzz import fuzz,process

def extract_skills(clean_text:str):
    found_skills = set()
    text = clean_text.lower()

# this words are the collections of tokens of words in a text this is called tokenization
    words = re.findall(r"\b\w+\b",text)

    for category,skills_dict in SKILLS_TAXONOMY.items():
        for standard_name,variants in skills_dict.items():
            match_found=False
            for variant in variants:

                # first we check exact match for speedy checking
                if re.search(rf"\b{re.escape(variant)}\b",text):
                    found_skills.add(standard_name)
                    match_found=True
                    break

                if len(variant)>3:
                    # if exact match not found then we use fuzzy logic using thefuzz library
                    best_match, score = process.extractOne(variant,words,scorer=fuzz.ratio) 

                    if score >= 90:
                        found_skills.add(standard_name)
                        match_found=True
                        break

            if match_found:
                continue

    return found_skills


def extract_contact(clean_text:str):
    text = clean_text.lower()
    found_contact = {"email": "", "phone": "", "linkedin": "", "github": ""}

    email_match = re.search(CONTACT_PATTERNS["email"],clean_text,re.IGNORECASE)
    if email_match:
        found_contact["email"]=email_match.group()

    phone_match = re.search(CONTACT_PATTERNS["phone"],clean_text)
    if phone_match:
        found_contact["phone"]=phone_match.group()

    for platform in ["linkedin", "github"]:
        link_match = re.search(CONTACT_PATTERNS[platform],clean_text, re.IGNORECASE)
        if link_match:
            found_contact[platform]=link_match.group()
    
    return found_contact

def extract_education(clean_text:str):
    education_keywords = ["education", "academic", "qualifications", "university", "college"]
    exclusion_list = ["mastering", "masterclass", "scrum master", "taskmaster"]

    text = clean_text.lower()
    found_education = {
        "degrees":set(),
        "streams":set()
    }

    search_area = text
    for key in education_keywords:
        if key in text:
            start_index = text.find(key)
            search_area = text[start_index : start_index + 600] # Narrow the search
            break

    # 2. Filtering Search Area (Exclusion)
    for word in exclusion_list:
        search_area = search_area.replace(word, "IGNORE")

    # for finding degrees
    for degree_level,patterns in EDUCATION_TAXONOMY["degrees"].items():
        for pattern in patterns:
            if re.search(pattern, search_area):
                found_education["degrees"].add(degree_level)
                break
    
    # for finding streams
    for stream_name,patterns in EDUCATION_TAXONOMY["streams"].items():
        for pattern in patterns:
            if re.search(pattern,search_area):
                found_education["streams"].add(stream_name)
                break

    return {
        "degrees":list(found_education["degrees"]),
        "streams":list(found_education["streams"])
    }


def extract_experience(clean_text:str):
    text = clean_text.lower()

    found_job_title = []
    found_action_verbs = []

    for job_title in EXPERIENCE_TAXONOMY["job_titles"]:
        if re.search(rf"\b{re.escape(job_title.lower())}\b",text):
            found_job_title.append(job_title)

    for action_verb in EXPERIENCE_TAXONOMY["action_verbs"]:
        if re.search(rf"\b{re.escape(action_verb.lower())}\b",text):
            found_action_verbs.append(action_verb)

    metrics = re.findall(EXPERIENCE_TAXONOMY["metrics_pattern"], text, re.IGNORECASE)
    
    return {
        "job_titles":list(set(found_job_title)),
        "action_verbs":list(set(found_action_verbs)),
        "metrics":metrics,
        "total_impact_count":len(metrics)
    }
