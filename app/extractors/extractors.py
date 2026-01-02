# keyword extraction
import re
from thefuzz import fuzz

def extract_skills(text:str)->list:
    text = text.lower()

    skills = {
        "programming_languages": {
            "python": ["python", "py", "python3"],
            "javascript": ["javascript", "js", "ecmascript"],
            "typescript": ["typescript", "ts"],
            "java": ["java", "j2ee", "core java"],
            "cpp": ["c++", "cpp", "c plus plus"],
            "csharp": ["c#", "c-sharp", "c sharp"],
            "golang": ["golang", "go language"],
            "php": ["php"],
            "ruby": ["ruby", "ror", "ruby on rails"],
            "restful api": ["rest api", "restful", "apis"],
            "html5": ["html", "html5", "web technologies"],
            "css3": ["css", "css3", "sass", "less"]
        },
        "web_frameworks": {
            "react": ["react", "react.js", "reactjs"],
            "angular": ["angular", "angularjs", "angular.js"],
            "vue": ["vue", "vue.js", "vuejs"],
            "node.js": ["node", "node.js", "nodejs","Node.js","Nodejs"],
            "Node.js": ["node", "node.js", "nodejs","Node.js","Nodejs"],
            "express.js": ["express", "expressjs", "express.js"],
            "django": ["django"],
            "flask": ["flask"],
            "fastapi": ["fastapi"],
            "spring boot": ["spring", "springboot", "spring framework"]
        },
        "databases": {
            "postgresql": ["postgresql", "postgres", "psql"],
            "mysql": ["mysql", "sql"],
            "mongodb": ["mongodb", "mongo", "nosql"],
            "redis": ["redis"],
            "oracle": ["oracle db"],
            "sqlite": ["sqlite"]
        },
        "cloud_devops": {
            "aws": ["aws", "amazon web services", "ec2", "s3", "lambda"],
            "azure": ["azure", "microsoft azure"],
            "gcp": ["gcp", "google cloud", "google cloud platform"],
            "docker": ["docker", "containerization"],
            "kubernetes": ["kubernetes", "k8s"],
            "jenkins": ["jenkins", "ci/cd", "cicd"],
            "terraform": ["terraform"],
            "git": ["git", "github", "gitlab", "bitbucket"],
            "aws": ["aws", "amazon web services", "ec2", "s3", "lambda", "aws migration"]
        },
        "data_science_ai": {
            "machine_learning": ["ml", "machine learning", "deep learning"],
            "pytorch": ["pytorch"],
            "tensorflow": ["tensorflow", "tf"],
            "pandas": ["pandas"],
            "numpy": ["numpy"],
            "scikit_learn": ["scikit-learn", "sklearn"],
            "nlp": ["nlp", "natural language processing"]
        },
        "soft_skills": {
            "leadership": ["leadership", "team management"],
            "communication": ["communication skills", "verbal communication"],
            "problem_solving": ["problem solving", "analytical skills"],
            "agile": ["agile", "scrum", "kanban"]
        }
    }

    found_skills = set()
    for category,skills_dict in skills.items():
        for standard_name, variants in skills_dict.items():
            for variant in variants:
                variant_clean = variant.lower()
                # using regex or in oprtr
                if variant_clean in text:
                    found_skills.add(standard_name)
                    break

                # using thefuzz library
                words = text.split()
                for word in words:
                    if fuzz.ratio(variant_clean,word) >90:
                        found_skills.add(standard_name)
                        break
                    
    return list(found_skills)




def extract_contacts(text:str)->dict:

    text = text.lower()

    contacts = {
        "email": {
            "pattern": "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}",
            "multiple": False
        },
        "phone": {
            "pattern":  r"\+?\d{10,13}",
            "multiple": True
        },
        "linkedin": {
            "pattern": "linkedin\\.com/in/[a-zA-Z0-9-_%]+",
            "multiple": False
        },
        "github": {
            "pattern": "github\\.com/[a-zA-Z0-9-_%]+",
            "multiple": False
        }
    }

    found_contacts = {}

    for contact,options in contacts.items():
        pattern = options["pattern"]
        multiple = options["multiple"]

        matches = re.findall(pattern,text)

        if matches:
            if multiple:
                found_contacts[contact] = matches
            else:
                found_contacts[contact] = matches[0]

    return found_contacts


def extract_education(text:str)->dict:
    text = text.lower()
    education_map = {
        "degrees": {
            "bachelor": [r"b\.tech", r"btech", r"b\.e", r"be", r"b\.sc", r"bsc", r"bca", r"bachelors?", r"undergraduate"],
            "master": [r"m\.tech", r"mtech", r"m\.e", r"me", r"m\.sc", r"msc", r"mca", r"masters?", r"postgraduate"],
            "phd": [r"phd", r"doctorate", r"p\.h\.d"],
            "diploma": [r"diploma"]
        },
        "streams": {
            "computer_science": [r"computer science", r"cse", r"information technology", r"it", r"software engineering"],
            "electronics": [r"electronics", r"ece", r"electrical", r"eee"],
            "mechanical": [r"mechanical", r"mech"],
            "civil": [r"civil"]
        }
    }

    found_degrees = set()
    found_streams = set()
    
    for degree_type,keywords in education["degrees"].items():
        for deg in keywords:
            if deg in text:
                found_degrees.append(degree_type)
                break
    
    for stream_type,keywords in education["streams"].items():
        for stream in keywords:
            if stream in text:
                found_streams.append(stream_type)
                break

    institution_present = any(
        inst in text for inst in education["institutions_keywords"]
    )


    found_year = re.findall(education["year_pattern"],text)

    return {
        "degrees":found_degrees,
        "streams":found_streams,
        "institution_keyword":institution_present,
        "year":found_year
    }


def extract_experience(text:str)->dict:
    text = text.lower()

    experience = {
        "job_titles": [
            "software engineer",
            "backend developer",
            "frontend developer",
            "full stack developer",
            "intern",
            "developer",
            "engineer",
            "data analyst",
            "data scientist",
            "machine learning engineer"
        ],

        "employment_keywords": [
            "company",
            "organization",
            "employer",
            "client"
        ],

        "action_verbs": [
            "developed",
            "designed",
            "implemented",
            "built",
            "optimized",
            "maintained",
            "created",
            "deployed",
            "led",
            "worked",
            "contributed"
        ],

        "duration_patterns": [
            r"(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+(?:19|20)\d{2}"
        ],

        "metrics_pattern": r"\b\d{2,}%|\b\d+\+"
    }

    found_job_title = []
    found_emp_keywords = []
    found_action = []
    found_duration_pattern = []
    found_metrics = None

    for title in experience["job_titles"]:
        if title in text:
            found_job_title.append(title)
    
    for action in experience["action_verbs"]:
        if action in text:
            found_action.append(action)

    for emp_key in experience["employment_keywords"]:
        if emp_key in text:
            found_emp_keywords.append(emp_key)
    
    for duration_pattern in experience["duration_patterns"]:
        found_duration_pattern.extend(
            re.findall(duration_pattern,text)
        )

    found_metrics = re.findall(experience["metrics_pattern"],text)

    return {
        "job_titles": found_job_title,
        "employment_keywords": found_emp_keywords,
        "action_verbs": found_action,
        "durations": found_duration_pattern,
        "metrics": found_metrics
    }