"""
=========================================================
AI Resume Screener
Skill Confidence Calculator
=========================================================
"""

import re


# ==========================================================
# Skill Confidence Calculator
# ==========================================================

def calculate_skill_confidence(resume_text, skills):
    """
    Calculates confidence score based on
    frequency of detected skills in resume.
    Returns an overall confidence score (0-100).
    """

    if not resume_text:
        return 0

    if not skills:
        return 0

    text = resume_text.lower()

    total_occurrences = 0

    for skill in skills:

        pattern = re.escape(skill.lower())

        matches = re.findall(pattern, text)

        total_occurrences += len(matches)

    # ------------------------------------------
    # Confidence Score
    # ------------------------------------------

    if len(skills) == 0:
        return 0

    average = total_occurrences / len(skills)

    confidence = min(100, round(average * 20))

    return confidence


# ==========================================================
# Individual Skill Confidence
# ==========================================================

def get_skill_breakdown(resume_text, skills):
    """
    Returns confidence for every skill.
    """

    if not resume_text:
        return {}

    text = resume_text.lower()

    breakdown = {}

    for skill in skills:

        pattern = re.escape(skill.lower())

        count = len(re.findall(pattern, text))

        score = min(100, count * 25)

        breakdown[skill] = score

    return breakdown


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    sample = """

    Python Python Python

    Flask

    SQL SQL

    Docker

    AWS

    """

    skills = [

        "Python",

        "Flask",

        "SQL",

        "Docker",

        "AWS"

    ]

    print("Overall Confidence:")
    print(calculate_skill_confidence(sample, skills))

    print("\nBreakdown:")
    print(get_skill_breakdown(sample, skills))