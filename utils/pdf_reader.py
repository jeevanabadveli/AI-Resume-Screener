"""
=========================================================
HireVision AI Resume Screener
PDF Reader Module
=========================================================
"""

import fitz
import pdfplumber
import tempfile
import os


def clean_text(text):

    if not text:
        return ""

    text = text.replace("\n", " ")
    text = text.replace("\t", " ")
    text = " ".join(text.split())

    return text.strip()


def extract_text_pymupdf(pdf_path):

    text = ""

    document = fitz.open(pdf_path)

    for page in document:
        text += page.get_text()

    document.close()

    return clean_text(text)


def extract_text_pdfplumber(pdf_path):

    text = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return clean_text(text)


def extract_text_from_pdf(pdf_path):

    text = extract_text_pymupdf(pdf_path)

    if len(text) < 20:
        text = extract_text_pdfplumber(pdf_path)

    return clean_text(text)


# ===================================================
# THIS FUNCTION IS REQUIRED BY app.py
# ===================================================

def extract_text_from_upload(uploaded_file):
    """
    Accepts Flask uploaded file OR file object.
    """

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:

        uploaded_file.seek(0)

        tmp.write(uploaded_file.read())

        temp_path = tmp.name

    try:

        text = extract_text_from_pdf(temp_path)

    finally:

        os.remove(temp_path)

    return text