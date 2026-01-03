# 1. Skills Taxonomy with Aliases
SKILLS_TAXONOMY = {
    "programming_languages": {
        "python": ["python", "py", "python3", "fastapi", "django", "flask"],
        "javascript": ["javascript", "js", "ecmascript", "es6"],
        "typescript": ["typescript", "ts"],
        "java": ["java", "j2ee", "core java", "spring boot", "hibernate"],
        "cpp": ["c++", "cpp", "c plus plus"],
        "csharp": ["c#", "c-sharp", "c sharp", ".net"],
        "golang": ["golang", "go language"],
        "php": ["php", "laravel", "wordpress"],
        "ruby": ["ruby", "ror", "ruby on rails"],
        "restful api": ["rest api", "restful", "apis", "json api", "http methods"],
        "html5": ["html", "html5", "semantic html"],
        "css3": ["css", "css3", "sass", "less", "tailwind", "bootstrap", "flexbox"]
    },
    "web_frameworks": {
        "react": ["react", "react.js", "reactjs", "next.js", "redux"],
        "angular": ["angular", "angularjs", "angular.js"],
        "vue": ["vue", "vue.js", "vuejs", "nuxt.js"],
        "node.js": ["node", "node.js", "nodejs"],
        "express.js": ["express", "expressjs", "express.js"],
        "django": ["django", "django rest framework", "drf"],
        "flask": ["flask"],
        "fastapi": ["fastapi"],
        "spring boot": ["spring", "springboot", "spring framework"]
    },
    "databases": {
        "postgresql": ["postgresql", "postgres", "psql"],
        "mysql": ["mysql", "sql", "mariadb"],
        "mongodb": ["mongodb", "mongo", "nosql", "mongoose"],
        "redis": ["redis", "caching"],
        "oracle": ["oracle db", "pl/sql"],
        "sqlite": ["sqlite"]
    },
    "cloud_devops": {
        "aws": ["aws", "amazon web services", "ec2", "s3", "lambda", "aws migration", "rds", "iam"],
        "azure": ["azure", "microsoft azure", "azure devops"],
        "gcp": ["gcp", "google cloud", "google cloud platform", "firebase"],
        "docker": ["docker", "containerization", "docker-compose"],
        "kubernetes": ["kubernetes", "k8s", "helm"],
        "jenkins": ["jenkins", "ci/cd", "cicd", "github actions"],
        "terraform": ["terraform", "infrastructure as code", "iac"],
        "git": ["git", "github", "gitlab", "bitbucket", "version control"]
    },
    "data_science_ai": {
        "machine_learning": ["ml", "machine learning", "deep learning", "neural networks"],
        "pytorch": ["pytorch"],
        "tensorflow": ["tensorflow", "tf", "keras"],
        "pandas": ["pandas"],
        "numpy": ["numpy"],
        "scikit_learn": ["scikit-learn", "sklearn"],
        "nlp": ["nlp", "natural language processing", "llm", "transformers"]
    },
    "soft_skills": {
        "leadership": ["leadership", "team management", "mentoring"],
        "communication": ["communication skills", "verbal communication", "presentation"],
        "problem_solving": ["problem solving", "analytical skills", "critical thinking"],
        "agile": ["agile", "scrum", "kanban", "jira"]
    }
}

# 2. Contact Patterns (Regex)
CONTACT_PATTERNS = {
    "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "phone": r"\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}",
    "linkedin": r"linkedin\.com/in/[a-zA-Z0-9-_%]+",
    "github": r"github\.com/[a-zA-Z0-9-_%]+"
}

# 3. Education Map
EDUCATION_TAXONOMY = {
    "degrees": {
        "bachelor": [r"\bb\.tech\b", r"\bbtech\b", r"\bb\.e\b", r"\bbe\b", r"\bbachelors?\b"],
        "master": [r"\bm\.tech\b", r"\bmtech\b", r"\bm\.sc\b", r"\bmasters?(?!\s+classes|ing)\b"], # Negative lookahead
        "phd": [r"\bphd\b", r"\bp\.h\.d\b"]
    },
    "streams": {
        "computer_science": [r"computer science", r"cse", r"information technology", r"it", r"software engineering"],
        "electronics": [r"electronics", r"ece", r"electrical", r"eee"],
        "mechanical": [r"mechanical", r"mech"],
        "civil": [r"civil"]
    }
}

# 4. Experience Keywords
EXPERIENCE_TAXONOMY = {
    "job_titles": [
        "software engineer", "backend developer", "frontend developer", 
        "full stack developer", "intern", "developer", "engineer", 
        "data analyst", "data scientist", "machine learning engineer",
        "sde", "technical lead", "system architect"
    ],
    "action_verbs": [
        "developed", "designed", "implemented", "built", "optimized", 
        "maintained", "created", "deployed", "led", "worked", "contributed",
        "reduced", "increased", "managed", "collaborated"
    ],
    "metrics_pattern": r"(\d{1,3}%\s?(?:increase|decrease|reduction|growth)?|\d+\+\s?(?:problems|users|clients|projects|repos)?|(?:\$|rs\.?|₹)\s?\d+[k|m|b]?)"
}
