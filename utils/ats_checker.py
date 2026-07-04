"""
=========================================================
AI Resume Screener
ATS Compatibility Checker
=========================================================
"""

import re


# ==========================================================
# ATS Checker
# ==========================================================

def check_ats_compatibility(resume_text):
    """
    Analyze resume for ATS compatibility.
    """

    if not resume_text:

        return {

            "score": 0,

            "rating": "Poor",

            "passed": False,

            "issues": ["Resume text is empty."],

            "word_count": 0

        }

    text = resume_text.strip()

    text_lower = text.lower()

    issues = []

    score = 100

    # ------------------------------------------------------
    # Word Count
    # ------------------------------------------------------

    word_count = len(text.split())

    if word_count < 200:

        issues.append("Resume is too short (less than 200 words).")

        score -= 20

    elif word_count > 1200:

        issues.append("Resume is too long (more than 1200 words).")

        score -= 10

    # ------------------------------------------------------
    # Email
    # ------------------------------------------------------

    email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    if not re.search(email_pattern, text):

        issues.append("Email address not found.")

        score -= 15

    # ------------------------------------------------------
    # Phone
    # ------------------------------------------------------

    phone_pattern = r"(\+?\d[\d\s\-]{8,15})"

    if not re.search(phone_pattern, text):

        issues.append("Phone number not found.")

        score -= 10

    # ------------------------------------------------------
    # Required Sections
    # ------------------------------------------------------

    required_sections = [

        "education",

        "experience",

        "skills"

    ]

    for section in required_sections:

        if section not in text_lower:

            issues.append(f"Missing section: {section.title()}")

            score -= 10

    # ------------------------------------------------------
    # Rating
    # ------------------------------------------------------

    score = max(0, min(100, score))

    if score >= 85:

        rating = "Excellent"

    elif score >= 70:

        rating = "Good"

    elif score >= 50:

        rating = "Average"

    else:

        rating = "Poor"

    passed = score >= 60

    return {

        "score": score,

        "rating": rating,

        "passed": passed,

        "issues": issues,

        "word_count": word_count

    }


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    sample = """
    John Doe

    Email: john@example.com

    Phone: +91 9876543210

    Education

    B.Tech Computer Science

    Experience

    Python Developer

    Skills

    Python
    Flask
    SQL
    AWS
    Docker
    """

    result = check_ats_compatibility(sample)

    print(result)