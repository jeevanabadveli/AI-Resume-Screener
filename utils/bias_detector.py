"""
=========================================================
AI Resume Screener
Bias Detector Module
=========================================================
"""

import re

# ==========================================================
# Bias Keywords
# ==========================================================

BIAS_KEYWORDS = [

    # Gender
    "male",
    "female",
    "man",
    "woman",
    "boy",
    "girl",
    "husband",
    "wife",

    # Age
    "young",
    "old",
    "age",
    "aged",
    "date of birth",
    "dob",

    # Religion
    "hindu",
    "muslim",
    "christian",
    "sikh",
    "buddhist",

    # Nationality
    "indian",
    "american",
    "british",
    "canadian",

    # Marital Status
    "married",
    "single",
    "divorced",
    "widowed"

]

# ==========================================================
# Bias Detection
# ==========================================================

def detect_bias_elements(resume_text):

    if not resume_text:

        return {

            "bias_score": 100,

            "bias_risk": "Unknown",

            "detected": [],

            "total_bias_elements": 0,

            "is_bias_free": True

        }

    text = resume_text.lower()

    detected = []

    for keyword in BIAS_KEYWORDS:

        pattern = r"\b" + re.escape(keyword) + r"\b"

        if re.search(pattern, text):

            detected.append(keyword)

    detected = sorted(list(set(detected)))

    total = len(detected)

    score = max(0, 100 - total * 15)

    if total == 0:

        risk = "Low"

    elif total <= 2:

        risk = "Medium"

    else:

        risk = "High"

    return {

        "bias_score": score,

        "bias_risk": risk,

        "detected": detected,

        "total_bias_elements": total,

        "is_bias_free": total == 0

    }


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    sample = """

    Name : John

    Male

    Married

    Indian

    """

    result = detect_bias_elements(sample)

    print(result)