# keyword extraction
import re

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
            "ruby": ["ruby", "ror", "ruby on rails"]
        },
        "web_frameworks": {
            "react": ["react", "react.js", "reactjs"],
            "angular": ["angular", "angularjs", "angular.js"],
            "vue": ["vue", "vue.js", "vuejs"],
            "node": ["node", "node.js", "nodejs"],
            "express": ["express", "expressjs", "express.js"],
            "django": ["django"],
            "flask": ["flask"],
            "fastapi": ["fastapi"]
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
            "git": ["git", "github", "gitlab", "bitbucket"]
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

    found_skills = []
    for category in skills.values():
        for skill_name, variants in category.items():
            for variant in variants:
                # \b (word boundary) use karein taaki 'C' skill 'Cat' mein match na ho jaye
                pattern = rf"\b{re.escape(variant.lower())}\b"
                if re.search(pattern, text):
                    found_skills.append(skill_name)
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
    education = {
        "degrees": {
            "bachelor": [
            "bachelor",
            "bachelors",
            "b.tech",
            "btech",
            "b.e",
            "be",
            "b.sc",
            "bsc",
            "bca"
            ],
            "master": [
            "master",
            "masters",
            "m.tech",
            "mtech",
            "m.e",
            "me",
            "m.sc",
            "msc",
            "mca"
            ],
            "phd": [
            "phd",
            "doctorate"
            ],
            "diploma": [
            "diploma"
            ]
        },

        "streams": {
            "computer_science": [
            "computer science",
            "cse",
            "information technology",
            "it",
            "software engineering"
            ],
            "electronics": [
            "electronics",
            "ece",
            "electrical",
            "eee"
            ],
            "mechanical": [
            "mechanical",
            "mech"
            ],
            "civil": [
            "civil"
            ]
        },

         "institutions_keywords": [
            "university",
            "college",
            "institute",
            "school"
        ],

        "year_pattern": r"\b(?:19|20)\d{2}\b"

        }

    found_degrees = []
    found_streams = []
    institution = False
    
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