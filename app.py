# ==========================================================
# AI Resume Screener
# Part 1
# Imports + Config + Database + Helper Functions
# ==========================================================

import os
import json
import sqlite3

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    Response,
    send_from_directory
)

from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# ==========================================================
# Import Utility Modules
# ==========================================================

from utils.pdf_reader import extract_text_from_upload
from utils.skill_extractor import analyze_resume
from utils.matcher import (
    calculate_match_score,
    get_skill_gap,
    rank_resumes
)

from utils.ats_checker import check_ats_compatibility
from utils.bias_detector import detect_bias_elements
from utils.fake_resume_detector import detect_fake_resume
from utils.skill_confidence import calculate_skill_confidence

from utils.interview_generator import (
    generate_interview_questions,
    generate_improvement_tips
)

from utils.pdf_report import generate_pdf_report

# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()

# ==========================================================
# Flask App
# ==========================================================

app = Flask(__name__)

app.secret_key = os.getenv(
    "SECRET_KEY",
    "resume-screener-secret-key"
)

# ==========================================================
# Upload Folder
# ==========================================================

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {"pdf"}

# ==========================================================
# SQLite Database
# ==========================================================

DATABASE = "resume_screener.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = get_db()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resumes (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            candidate_name TEXT,

            filename TEXT,

            ats_score INTEGER,

            match_score INTEGER,

            authenticity INTEGER,

            bias_score INTEGER,

            confidence INTEGER,

            skills TEXT,

            education TEXT,

            experience TEXT,

            recommendation TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    conn.commit()

    conn.close()


init_db()

# ==========================================================
# Helper Functions
# ==========================================================

def allowed_file(filename):

    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def save_resume_record(data):

    conn = get_db()

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO resumes(

            candidate_name,

            filename,

            ats_score,

            match_score,

            authenticity,

            bias_score,

            confidence,

            skills,

            education,

            experience,

            recommendation

        )

        VALUES(?,?,?,?,?,?,?,?,?,?,?)

    """, (

        data["candidate_name"],

        data["filename"],

        data["ats_score"],

        data["match_score"],

        data["authenticity"],

        data["bias_score"],

        data["confidence"],

        json.dumps(data["skills"]),

        json.dumps(data["education"]),

        str(data["experience"]),

        data["recommendation"]

    ))

    conn.commit()

    conn.close()


def get_resume_history():

    conn = get_db()

    rows = conn.execute("""

        SELECT *

        FROM resumes

        ORDER BY id DESC

    """).fetchall()

    conn.close()

    return [dict(row) for row in rows]
    # ==========================================================
# PAGE ROUTES
# ==========================================================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/analyze")
def analyze_page():
    return render_template("analyze.html")


@app.route("/ranking")
def ranking_page():
    return render_template("ranking.html")


@app.route("/interview")
def interview_page():
    return render_template("interview.html")


@app.route("/report")
def report_page():
    return render_template("report.html")


@app.route("/history")
def history_page():
    return render_template("history.html")


# ==========================================================
# DOWNLOAD UPLOADED RESUMES
# ==========================================================

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )


# ==========================================================
# DASHBOARD API
# ==========================================================

@app.route("/api/dashboard")
def api_dashboard():

    history = get_resume_history()

    total = len(history)

    if total == 0:

        return jsonify({
            "total_resumes": 0,
            "average_ats": 0,
            "reports_generated": 0,
            "top_candidate": "None"
        })

    average_ats = round(
        sum(r["ats_score"] for r in history) / total,
        2
    )

    top_candidate = max(
        history,
        key=lambda x: x["match_score"]
    )

    return jsonify({

        "total_resumes": total,

        "average_ats": average_ats,

        "reports_generated": total,

        "top_candidate": top_candidate["candidate_name"]

    })


# ==========================================================
# ANALYTICS API
# ==========================================================

@app.route("/api/analytics")
def api_analytics():

    history = get_resume_history()

    total = len(history)

    if total == 0:

        return jsonify({

            "total_resumes": 0,

            "average_ats": 0,

            "average_match": 0,

            "average_confidence": 0

        })

    average_ats = round(

        sum(r["ats_score"] for r in history) / total,

        2

    )

    average_match = round(

        sum(r["match_score"] for r in history) / total,

        2

    )

    average_confidence = round(

        sum(r["confidence"] for r in history) / total,

        2

    )

    return jsonify({

        "total_resumes": total,

        "average_ats": average_ats,

        "average_match": average_match,

        "average_confidence": average_confidence

    })


# ==========================================================
# HISTORY API
# ==========================================================

@app.route("/api/history")
def api_history():

    history = get_resume_history()

    result = []

    for row in history:

        result.append({

            "candidate_name": row["candidate_name"],

            "ats_score": row["ats_score"],

            "match_score": row["match_score"],

            "status": row["recommendation"],

            "date": row["created_at"]

        })

    return jsonify(result)


# ==========================================================
# LATEST RESULT API
# ==========================================================

@app.route("/api/result")
def api_result():

    conn = get_db()

    row = conn.execute("""

        SELECT *

        FROM resumes

        ORDER BY id DESC

        LIMIT 1

    """).fetchone()

    conn.close()

    if row is None:

        return jsonify({

            "candidate_name": "No Resume",

            "skills": [],

            "education": [],

            "experience": "",

            "ats": {
                "ats_score": 0
            },

            "match": {
                "overall_score": 0,
                "recommendation": "No Analysis",
                "missing_skills": []
            },

            "confidence": {
                "overall_confidence": 0
            },

            "bias": {
                "bias_score": 0
            },

            "fake": {
                "authenticity_score": 0
            }

        })

    return jsonify({

        "candidate_name": row["candidate_name"],

        "skills": json.loads(row["skills"]),

        "education": json.loads(row["education"]),

        "experience": row["experience"],

        "ats": {
            "ats_score": row["ats_score"]
        },

        "match": {
            "overall_score": row["match_score"],
            "recommendation": row["recommendation"],
            "missing_skills": []
        },

        "confidence": {
            "overall_confidence": row["confidence"]
        },

        "bias": {
            "bias_score": row["bias_score"]
        },

        "fake": {
            "authenticity_score": row["authenticity"]
        }

    })
    # ==========================================================
# AI RESUME ANALYSIS API (PART 3A)
# ==========================================================

@app.route("/api/analyze", methods=["POST"])
def api_analyze():

    try:

        # ---------------------------------------------
        # Validate Resume Upload
        # ---------------------------------------------

        if "resume" not in request.files:
            return jsonify({
                "success": False,
                "message": "Resume file is required."
            }), 400

        resume = request.files["resume"]

        job_description = request.form.get(
            "job_description",
            ""
        ).strip()

        if resume.filename == "":
            return jsonify({
                "success": False,
                "message": "Please select a resume."
            }), 400

        if not allowed_file(resume.filename):
            return jsonify({
                "success": False,
                "message": "Only PDF resumes are allowed."
            }), 400

        if job_description == "":
            return jsonify({
                "success": False,
                "message": "Job description is required."
            }), 400
        # ---------------------------------------------
        # Save Resume
        # ---------------------------------------------

        filename = secure_filename(resume.filename)

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        resume.save(filepath)

        # ---------------------------------------------
        # Extract Resume Text
        # ---------------------------------------------

        with open(filepath, "rb") as pdf_file:

            resume_text = extract_text_from_upload(pdf_file)

        if not resume_text:

            return jsonify({
                "success": False,
                "message": "Unable to extract text from resume."
            }), 400

        # ---------------------------------------------
        # Resume Analysis
        # ---------------------------------------------

        resume_analysis = analyze_resume(
            resume_text
        )

        jd_analysis = analyze_resume(
            job_description
        )

        candidate_name = os.path.splitext(
            filename
        )[0]

        # ---------------------------------------------
        # ATS Check
        # ---------------------------------------------

        ats_result = check_ats_compatibility(
            resume_text
        )

        # ---------------------------------------------
        # Resume Match Score
        # ---------------------------------------------

        match_score = calculate_match_score(
            resume_text,
            job_description
        )

        # ---------------------------------------------
        # Skill Gap Analysis
        # ---------------------------------------------

        skill_gap = get_skill_gap(
            resume_analysis["skills"],
            jd_analysis["skills"]
        )

        # ---------------------------------------------
        # Store Intermediate Results
        # ---------------------------------------------

        analysis_data = {

            "candidate_name": candidate_name,

            "filename": filename,

            "resume_text": resume_text,

            "resume_analysis": resume_analysis,

            "jd_analysis": jd_analysis,

            "ats_result": ats_result,

            "match_score": match_score,

            "skill_gap": skill_gap

        }
                # =========================================================
        # AI ENHANCEMENTS
        # =========================================================

        bias_result = detect_bias_elements(
            resume_text
        )

        fake_result = detect_fake_resume(
            resume_text
        )

        confidence_score = calculate_skill_confidence(
            resume_text,
            resume_analysis["skills"]
        )

        interview_result = generate_interview_questions(
            resume_analysis["skills"],
            resume_analysis["education"],
            job_description
        )

        tips_result = generate_improvement_tips(
            resume_analysis["skills"],
            skill_gap["missing_skills"],
            resume_analysis["experience_years"]
        )

        # =========================================================
        # Final Scores
        # =========================================================

        ats_score = ats_result["score"]

        recommendation = (
            "Strong Match"
            if match_score >= 80 else
            "Moderate Match"
            if match_score >= 60 else
            "Needs Improvement"
        )

        # =========================================================
        # Save Result
        # =========================================================

        save_resume_record({

            "candidate_name": candidate_name,

            "filename": filename,

            "ats_score": ats_score,

            "match_score": match_score,

            "authenticity": fake_result["authenticity_score"],

            "bias_score": bias_result["bias_score"],

            "confidence": confidence_score,

            "skills": resume_analysis["skills"],

            "education": resume_analysis["education"],

            "experience": resume_analysis["experience_years"],

            "recommendation": recommendation

        })

        # =========================================================
        # JSON Response
        # =========================================================

        return jsonify({

            "success": True,

            "candidate_name": candidate_name,

            "skills": resume_analysis["skills"],

            "education": resume_analysis["education"],

            "experience_years": resume_analysis["experience_years"],

            "matched_skills": skill_gap["matched_skills"],

            "missing_skills": skill_gap["missing_skills"],

            "ats": {

                "ats_score": ats_score,

                "rating": ats_result["rating"],

                "passed": ats_result["passed"],

                "issues": ats_result["issues"]

            },

            "match": {

                "overall_score": match_score,

                "recommendation": recommendation,

                "missing_skills": skill_gap["missing_skills"]

            },

            "confidence": {

                "overall_confidence": confidence_score

            },

            "bias": {

                "bias_score": bias_result["bias_score"],

                "bias_risk": bias_result["bias_risk"]

            },

            "fake": {

                "authenticity_score": fake_result["authenticity_score"],

                "verdict": fake_result["verdict"]

            },

            "interview_questions": interview_result.get(
                "questions",
                []
            ),

            "improvement_tips": tips_result.get(
                "tips",
                []
            )

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500
        # ==========================================================
# RESUME RANKING API
# ==========================================================

@app.route("/api/rank", methods=["POST"])
def api_rank():

    try:

        job_description = request.form.get(
            "job_description",
            ""
        ).strip()

        resumes = request.files.getlist("resumes")

        if not job_description:

            return jsonify({
                "success": False,
                "message": "Job description is required."
            }), 400

        if len(resumes) == 0:

            return jsonify({
                "success": False,
                "message": "Please upload resumes."
            }), 400

        resume_list = []

        for resume in resumes:

            if resume and allowed_file(resume.filename):

                text = extract_text_from_upload(resume)

                if text:

                    resume_list.append({

                        "name": resume.filename,

                        "text": text

                    })

        if len(resume_list) == 0:

            return jsonify({
                "success": False,
                "message": "No valid resumes found."
            }), 400

        ranked = rank_resumes(
            resume_list,
            job_description
        )

        return jsonify({

            "success": True,

            "ranked_resumes": ranked

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# ==========================================================
# PDF REPORT DOWNLOAD API
# ==========================================================

@app.route("/api/download-report", methods=["POST"])
def api_download_report():

    try:

        data = request.get_json()

        if data is None:

            return jsonify({

                "success": False,

                "message": "No report data received."

            }), 400

        pdf_bytes = generate_pdf_report(data)

        return Response(

            pdf_bytes,

            mimetype="application/pdf",

            headers={

                "Content-Disposition":
                "attachment; filename=Resume_Report.pdf"

            }

        )

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# ==========================================================
# INTERVIEW QUESTION API
# ==========================================================

@app.route("/api/interview", methods=["POST"])
def api_interview():

    try:

        data = request.get_json()

        if data is None:

            return jsonify({

                "success": False,

                "message": "Invalid request."

            }), 400

        skills = data.get("skills", [])

        education = data.get("education", [])

        job_description = data.get(
            "job_description",
            ""
        )

        result = generate_interview_questions(

            skills,

            education,

            job_description

        )

        return jsonify({

            "success": True,

            "questions": result.get(
                "questions",
                []
            )

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500
        # ==========================================================
# ERROR HANDLERS
# ==========================================================

@app.errorhandler(404)
def page_not_found(error):

    return jsonify({

        "success": False,

        "error": "Page not found.",

        "status": 404

    }), 404


@app.errorhandler(500)
def internal_server_error(error):

    return jsonify({

        "success": False,

        "error": "Internal Server Error.",

        "status": 500

    }), 500


# ==========================================================
# HEALTH CHECK API
# ==========================================================

@app.route("/api/health")
def api_health():

    return jsonify({

        "success": True,

        "message": "AI Resume Screener API is running.",

        "version": "2.0"

    })


# ==========================================================
# APPLICATION ENTRY POINT
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("🚀 AI Resume Screener Started Successfully")
    print("=" * 60)
    print("🌐 Home        : http://127.0.0.1:5000/")
    print("📊 Dashboard   : http://127.0.0.1:5000/dashboard")
    print("📈 Analytics   : http://127.0.0.1:5000/api/analytics")
    print("📜 History     : http://127.0.0.1:5000/history")
    print("❤️ Health API  : http://127.0.0.1:5000/api/health")
    print("=" * 60)

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
    