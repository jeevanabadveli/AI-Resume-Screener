"""
=========================================================
AI Resume Screener
Interview Question Generator
=========================================================
"""

# ==========================================================
# Skill-wise Questions
# ==========================================================

QUESTION_BANK = {

    "python": [
        "Explain Python decorators.",
        "What are Python generators?",
        "Difference between list and tuple?",
        "Explain Python OOP concepts."
    ],

    "java": [
        "Explain JVM, JRE and JDK.",
        "What is inheritance in Java?",
        "Difference between interface and abstract class?"
    ],

    "sql": [
        "Difference between DELETE, TRUNCATE and DROP.",
        "Explain SQL JOINs.",
        "What are indexes?"
    ],

    "mysql": [
        "Explain primary key and foreign key.",
        "What is normalization?"
    ],

    "html": [
        "Difference between HTML and HTML5.",
        "Explain semantic tags."
    ],

    "css": [
        "Difference between Flexbox and Grid.",
        "Explain CSS specificity."
    ],

    "javascript": [
        "Explain closures.",
        "Difference between let, var and const.",
        "What is event bubbling?"
    ],

    "react": [
        "Explain React Hooks.",
        "What is Virtual DOM?"
    ],

    "flask": [
        "What is Flask?",
        "Explain Flask routing.",
        "What is Jinja2?"
    ],

    "django": [
        "Explain Django ORM.",
        "What are Django Models?"
    ],

    "machine learning": [
        "Difference between supervised and unsupervised learning.",
        "Explain overfitting.",
        "What is cross validation?"
    ],

    "deep learning": [
        "What is a neural network?",
        "Explain backpropagation."
    ],

    "pandas": [
        "Difference between loc and iloc.",
        "How do you handle missing values?"
    ],

    "numpy": [
        "Difference between array and list.",
        "Explain broadcasting."
    ],

    "power bi": [
        "Explain DAX.",
        "What are calculated columns?"
    ],

    "tableau": [
        "Difference between live and extract connection.",
        "Explain dashboards."
    ],

    "aws": [
        "What is EC2?",
        "Difference between EC2 and Lambda?"
    ],

    "docker": [
        "Difference between Docker Image and Container.",
        "Explain Dockerfile."
    ]
}

# ==========================================================
# Interview Generator
# ==========================================================

def generate_interview_questions(skills, education, job_description, num_questions=10):

    questions = []

    if skills:

        for skill in skills:

            key = skill.lower()

            if key in QUESTION_BANK:

                questions.extend(QUESTION_BANK[key])

    if len(questions) == 0:

        questions = [

            "Introduce yourself.",

            "Tell me about your final year project.",

            "What are your strengths?",

            "What are your weaknesses?",

            "Why should we hire you?",

            "Describe a challenging situation you faced.",

            "Where do you see yourself in 5 years?",

            "Explain one technical project."

        ]

    # Remove duplicates

    unique = []

    for q in questions:

        if q not in unique:

            unique.append(q)

    return {

        "questions": unique[:num_questions]

    }


# ==========================================================
# Resume Improvement Tips
# ==========================================================

def generate_improvement_tips(skills, missing_skills, experience):

    tips = []

    if len(skills) < 5:

        tips.append(
            "Add more technical skills relevant to your domain."
        )

    if missing_skills:

        tips.append(
            "Learn these missing skills: " +
            ", ".join(missing_skills)
        )

    if experience == 0:

        tips.append(
            "Include internships, certifications or academic projects."
        )

    elif experience < 2:

        tips.append(
            "Highlight measurable achievements from your work."
        )

    tips.append(
        "Keep your resume limited to 1-2 pages."
    )

    tips.append(
        "Quantify your achievements using numbers."
    )

    tips.append(
        "Tailor your resume for every job description."
    )

    tips.append(
        "Use ATS-friendly formatting."
    )

    return {

        "tips": tips

    }


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    skills = [

        "Python",

        "Flask",

        "SQL",

        "Docker"

    ]

    print(generate_interview_questions(

        skills,

        [],

        ""

    ))

    print()

    print(generate_improvement_tips(

        skills,

        ["AWS", "Git"],

        1

    ))