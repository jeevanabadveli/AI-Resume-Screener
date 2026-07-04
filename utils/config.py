"""
=========================================
HireVision AI Resume Screener
Configuration File
=========================================
"""

import os

# ==========================================
# PROJECT DIRECTORIES
# ==========================================

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

REPORT_FOLDER = os.path.join(BASE_DIR, "reports")

HISTORY_FOLDER = os.path.join(BASE_DIR, "history")

# ==========================================
# FILE SETTINGS
# ==========================================

ALLOWED_EXTENSIONS = {"pdf"}

MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# ==========================================
# ATS SETTINGS
# ==========================================

MIN_ATS_SCORE = 70

MAX_SKILLS = 25

# ==========================================
# COLORS
# ==========================================

PRIMARY_COLOR = "#7C3AED"

SECONDARY_COLOR = "#06B6D4"

SUCCESS_COLOR = "#22C55E"

WARNING_COLOR = "#F59E0B"

DANGER_COLOR = "#EF4444"

# ==========================================
# APP INFO
# ==========================================

APP_NAME = "HireVision AI"

VERSION = "2.0"

SECRET_KEY = "hirevision_ai_secret_key"