"""
=========================================================
AI Resume Screener
PDF Report Generator
=========================================================
"""

from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)


def generate_pdf_report(data):
    """
    Generates a PDF report from analysis data.
    Returns PDF bytes.
    """

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    # ======================================================
    # Title
    # ======================================================

    title = Paragraph(
        "<b><font size=18>AI Resume Analysis Report</font></b>",
        styles["Title"]
    )

    story.append(title)
    story.append(Spacer(1, 20))

    # ======================================================
    # Candidate
    # ======================================================

    candidate = data.get(
        "candidate_name",
        "Unknown Candidate"
    )

    story.append(
        Paragraph(
            f"<b>Candidate:</b> {candidate}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 12))

    # ======================================================
    # ATS
    # ======================================================

    ats = data.get("ats", {})

    story.append(
        Paragraph(
            "<b>ATS Analysis</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"ATS Score : {ats.get('ats_score',0)}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Rating : {ats.get('rating','N/A')}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 12))

    # ======================================================
    # Match
    # ======================================================

    match = data.get("match", {})

    story.append(
        Paragraph(
            "<b>Resume Match</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"Match Score : {match.get('overall_score',0)}%",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Recommendation : {match.get('recommendation','N/A')}",
            styles["Normal"]
        )
    )

    missing = match.get(
        "missing_skills",
        []
    )

    if missing:

        story.append(
            Paragraph(
                "<b>Missing Skills</b>",
                styles["Heading3"]
            )
        )

        story.append(
            Paragraph(
                ", ".join(missing),
                styles["Normal"]
            )
        )

    story.append(Spacer(1, 12))

    # ======================================================
    # Skills
    # ======================================================

    skills = data.get(
        "skills",
        []
    )

    story.append(
        Paragraph(
            "<b>Detected Skills</b>",
            styles["Heading2"]
        )
    )

    if skills:

        story.append(
            Paragraph(
                ", ".join(skills),
                styles["Normal"]
            )
        )

    else:

        story.append(
            Paragraph(
                "No skills detected.",
                styles["Normal"]
            )
        )

    story.append(Spacer(1, 12))

    # ======================================================
    # Education
    # ======================================================

    education = data.get(
        "education",
        []
    )

    story.append(
        Paragraph(
            "<b>Education</b>",
            styles["Heading2"]
        )
    )

    if education:

        story.append(
            Paragraph(
                ", ".join(education),
                styles["Normal"]
            )
        )

    else:

        story.append(
            Paragraph(
                "Not Available",
                styles["Normal"]
            )
        )

    story.append(Spacer(1, 12))

    # ======================================================
    # Confidence
    # ======================================================

    confidence = data.get(
        "confidence",
        {}
    )

    story.append(
        Paragraph(
            "<b>Skill Confidence</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"Confidence Score : {confidence.get('overall_confidence',0)}%",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 12))

    # ======================================================
    # Bias
    # ======================================================

    bias = data.get(
        "bias",
        {}
    )

    story.append(
        Paragraph(
            "<b>Bias Analysis</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"Bias Score : {bias.get('bias_score',0)}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Risk : {bias.get('bias_risk','N/A')}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 12))

    # ======================================================
    # Authenticity
    # ======================================================

    fake = data.get(
        "fake",
        {}
    )

    story.append(
        Paragraph(
            "<b>Resume Authenticity</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"Authenticity Score : {fake.get('authenticity_score',0)}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Verdict : {fake.get('verdict','N/A')}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 15))

    # ======================================================
    # Interview Questions
    # ======================================================

    questions = data.get(
        "interview_questions",
        []
    )

    if questions:

        story.append(
            Paragraph(
                "<b>Suggested Interview Questions</b>",
                styles["Heading2"]
            )
        )

        for question in questions:

            story.append(
                Paragraph(
                    f"• {question}",
                    styles["Normal"]
                )
            )

    story.append(Spacer(1, 15))

    # ======================================================
    # Tips
    # ======================================================

    tips = data.get(
        "improvement_tips",
        []
    )

    if tips:

        story.append(
            Paragraph(
                "<b>Resume Improvement Tips</b>",
                styles["Heading2"]
            )
        )

        for tip in tips:

            story.append(
                Paragraph(
                    f"• {tip}",
                    styles["Normal"]
                )
            )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "<font color='grey'>Generated by AI Resume Screener</font>",
            styles["Italic"]
        )
    )

    doc.build(story)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    sample = {

        "candidate_name": "John Doe",

        "skills": ["Python", "Flask", "SQL"],

        "education": ["B.Tech"],

        "ats": {
            "ats_score": 88,
            "rating": "Good"
        },

        "match": {
            "overall_score": 84,
            "recommendation": "Strong Match",
            "missing_skills": ["AWS"]
        },

        "confidence": {
            "overall_confidence": 92
        },

        "bias": {
            "bias_score": 98,
            "bias_risk": "Low"
        },

        "fake": {
            "authenticity_score": 95,
            "verdict": "Highly Authentic"
        },

        "interview_questions": [
            "Explain Python decorators.",
            "What is Flask?"
        ],

        "improvement_tips": [
            "Learn AWS.",
            "Add project metrics."
        ]

    }

    pdf = generate_pdf_report(sample)

    with open("sample_report.pdf", "wb") as f:
        f.write(pdf)

    print("PDF report generated successfully.")