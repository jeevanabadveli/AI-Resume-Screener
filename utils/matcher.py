"""
=========================================================
AI Resume Screener
Resume Matcher Module
=========================================================
"""

from difflib import SequenceMatcher


# ==========================================================
# Similarity Function
# ==========================================================

def similarity(a, b):
    """
    Returns similarity ratio between two strings.
    """

    return SequenceMatcher(
        None,
        a.lower(),
        b.lower()
    ).ratio()


# ==========================================================
# Match Score
# ==========================================================

def calculate_match_score(resume_text, job_description):
    """
    Calculate resume match score against job description.
    """

    if not resume_text or not job_description:
        return 0

    score = similarity(
        resume_text,
        job_description
    )

    return round(score * 100)


# ==========================================================
# Skill Gap Analysis
# ==========================================================

def get_skill_gap(resume_skills, jd_skills):

    resume_set = set(
        skill.lower()
        for skill in resume_skills
    )

    jd_set = set(
        skill.lower()
        for skill in jd_skills
    )

    matched = sorted(
        list(resume_set & jd_set)
    )

    missing = sorted(
        list(jd_set - resume_set)
    )

    return {

        "matched_skills": matched,

        "missing_skills": missing

    }


# ==========================================================
# Resume Ranking
# ==========================================================

def rank_resumes(resume_list, job_description):
    """
    Rank multiple resumes against a job description.
    """

    ranked = []

    for resume in resume_list:

        score = calculate_match_score(
            resume["text"],
            job_description
        )

        ranked.append({

            "candidate_name": resume["name"],

            "match_score": score,

            "recommendation": (
                "Strong Match"
                if score >= 80 else
                "Moderate Match"
                if score >= 60 else
                "Weak Match"
            )

        })

    ranked.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    for index, resume in enumerate(ranked):

        resume["rank"] = index + 1

    return ranked


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    resume = """
    Python
    Flask
    MySQL
    AWS
    Docker
    """

    jd = """
    Looking for Python Developer
    Flask
    AWS
    Git
    Docker
    """

    print(calculate_match_score(resume, jd))

    print(get_skill_gap(

        ["Python", "Flask", "Docker"],

        ["Python", "AWS", "Docker", "Git"]

    ))

    resumes = [

        {

            "name": "Alice.pdf",

            "text": "Python Flask AWS"

        },

        {

            "name": "Bob.pdf",

            "text": "Java Spring Boot"

        }

    ]

    print(rank_resumes(resumes, jd))