"""
=========================================================
AI Resume Screener
Fake Resume Detector
=========================================================
"""

import re


# ==========================================================
# Suspicious Keywords
# ==========================================================

SUSPICIOUS_KEYWORDS = [

    "expert in everything",
    "100% guaranteed",
    "world best",
    "perfect",
    "master of all",
    "no experience but expert",
    "fake",
    "dummy",
    "sample",
    "lorem ipsum"

]


# ==========================================================
# Authenticity Checker
# ==========================================================

def detect_fake_resume(resume_text):

    if not resume_text:

        return {

            "authenticity_score": 0,

            "verdict": "Invalid Resume",

            "verdict_color": "danger",

            "red_flags": [],

            "warnings": ["Resume text is empty."],

            "total_issues": 1

        }

    text = resume_text.lower()

    red_flags = []

    warnings = []

    # ------------------------------------------------------
    # Suspicious Keywords
    # ------------------------------------------------------

    for keyword in SUSPICIOUS_KEYWORDS:

        if keyword in text:

            red_flags.append(
                f"Suspicious phrase detected: {keyword}"
            )

    # ------------------------------------------------------
    # Email Check
    # ------------------------------------------------------

    email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    if not re.search(email_pattern, text):

        warnings.append("No email address found.")

    # ------------------------------------------------------
    # Phone Check
    # ------------------------------------------------------

    phone_pattern = r"(\+?\d[\d\s\-]{8,15})"

    if not re.search(phone_pattern, text):

        warnings.append("No phone number found.")

    # ------------------------------------------------------
    # Experience Check
    # ------------------------------------------------------

    experience_pattern = r"\b\d+\+?\s*(years|yrs|year)\b"

    if not re.search(experience_pattern, text):

        warnings.append("Experience information not found.")

    # ------------------------------------------------------
    # Education Check
    # ------------------------------------------------------

    education_keywords = [

        "b.tech",
        "btech",
        "b.e",
        "be",
        "m.tech",
        "mtech",
        "bsc",
        "msc",
        "bca",
        "mca",
        "phd"

    ]

    if not any(word in text for word in education_keywords):

        warnings.append("Education details not found.")

    # ------------------------------------------------------
    # Calculate Score
    # ------------------------------------------------------

    issues = len(red_flags) + len(warnings)

    authenticity_score = max(

        0,

        100 - (len(red_flags) * 20) - (len(warnings) * 8)

    )

    # ------------------------------------------------------
    # Verdict
    # ------------------------------------------------------

    if authenticity_score >= 90:

        verdict = "Highly Authentic"

        color = "success"

    elif authenticity_score >= 75:

        verdict = "Likely Authentic"

        color = "primary"

    elif authenticity_score >= 60:

        verdict = "Needs Manual Review"

        color = "warning"

    else:

        verdict = "Potentially Fake"

        color = "danger"

    return {

        "authenticity_score": authenticity_score,

        "verdict": verdict,

        "verdict_color": color,

        "red_flags": red_flags,

        "warnings": warnings,

        "total_issues": issues

    }


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    sample = """

    John Doe

    Email : john@gmail.com

    Phone : +91 9876543210

    B.Tech Computer Science

    Python Developer

    3 years experience

    """

    result = detect_fake_resume(sample)

    print(result)