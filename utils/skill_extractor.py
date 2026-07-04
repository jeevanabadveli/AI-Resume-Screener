"""
=========================================================
AI Resume Screener
Skill Extractor Module
=========================================================
"""

import re

# ==========================================================
# Skill Database
# ==========================================================

SKILLS = [

    # Programming
    "python",
    "java",
    "c",
    "c++",
    "c#",
    "javascript",
    "typescript",
    "php",
    "ruby",
    "go",
    "kotlin",
    "swift",
    "r",

    # Web
    "html",
    "css",
    "bootstrap",
    "tailwind",
    "react",
    "angular",
    "vue",
    "node.js",
    "express",

    # Database
    "mysql",
    "postgresql",
    "sqlite",
    "mongodb",
    "oracle",

    # Data Science
    "numpy",
    "pandas",
    "matplotlib",
    "seaborn",
    "scikit-learn",
    "tensorflow",
    "keras",
    "pytorch",
    "opencv",

    # Cloud
    "aws",
    "azure",
    "gcp",
    "docker",
    "kubernetes",

    # Tools
    "git",
    "github",
    "linux",
    "jira",
    "excel",
    "power bi",
    "tableau",

    # AI
    "machine learning",
    "deep learning",
    "nlp",
    "computer vision",
    "generative ai",
    "llm",

    # Soft Skills
    "communication",
    "leadership",
    "teamwork",
    "problem solving",
    "critical thinking"
]

# ==========================================================
# Education Keywords
# ==========================================================

EDUCATION = [

    "b.tech",
    "btech",
    "be",
    "b.e",
    "m.tech",
    "mtech",
    "me",
    "m.e",
    "bsc",
    "msc",
    "bca",
    "mca",
    "phd",
    "diploma"
]


# ==========================================================
# Skill Extraction
# ==========================================================

def extract_skills(text):

    if not text:
        return []

    text = text.lower()

    found = []

    for skill in SKILLS:

        if skill.lower() in text:

            found.append(skill)

    return sorted(list(set(found)))


# ==========================================================
# Education Extraction
# ==========================================================

def extract_education(text):

    if not text:
        return []

    text = text.lower()

    education = []

    for degree in EDUCATION:

        if degree in text:

            education.append(degree.upper())

    return list(set(education))


# ==========================================================
# Experience Extraction
# ==========================================================

def extract_experience(text):

    if not text:
        return 0

    text = text.lower()

    patterns = [

        r'(\d+)\+?\s*years',

        r'(\d+)\+?\s*yrs',

        r'(\d+)\s*year'

    ]

    years = []

    for pattern in patterns:

        matches = re.findall(pattern, text)

        for match in matches:

            years.append(int(match))

    if years:

        return max(years)

    return 0


# ==========================================================
# Resume Analyzer
# ==========================================================

def analyze_resume(text):

    skills = extract_skills(text)

    education = extract_education(text)

    experience = extract_experience(text)

    return {

        "skills": skills,

        "education": education,

        "experience_years": experience

    }


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    sample = """

    Python Developer

    Skills:
    Python
    Flask
    MySQL
    Docker
    AWS
    Machine Learning
    Git

    Education:
    B.Tech Computer Science

    Experience:
    3 years

    """

    print(analyze_resume(sample))