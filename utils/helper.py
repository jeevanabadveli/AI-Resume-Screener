"""
=========================================
Helper Functions
=========================================
"""

import os
import uuid


def allowed_file(filename):

    """
    Check whether uploaded file is PDF.
    """

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() == "pdf"
    )


def generate_unique_filename(filename):

    """
    Generate unique filename.
    """

    extension = filename.rsplit(".", 1)[1]

    unique_name = str(uuid.uuid4())

    return f"{unique_name}.{extension}"


def create_directory(folder):

    """
    Create folder if not exists.
    """

    if not os.path.exists(folder):

        os.makedirs(folder)


def format_percentage(score):

    """
    Convert float into percentage string.
    """

    return f"{round(score,2)}%"


def normalize_text(text):

    """
    Remove extra spaces.
    """

    return " ".join(text.split())