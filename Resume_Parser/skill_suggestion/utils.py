import spacy
#from PyPDF2 import PdfReader
from .models import Skill
import pymupdf4llm
import tempfile
import fitz  # PyMuPDF
import re

nlp = spacy.load("en_core_web_sm")

# def extract_text_from_pdf(file_obj):
#     reader = PdfReader(file_obj)
#     text = ""
#     for page in reader.pages:
#         text += page.extract_text() + " "
#     return text

def clean_markdown(md_text):
    return re.sub(r'[#\-\*`]', '', md_text)

def extract_text_from_pdf(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        for chunk in file.chunks():
            tmp.write(chunk)
        tmp_path = tmp.name

    doc = fitz.open(tmp_path)
    text = ""
    for page in doc:
        text += page.get_text()

          # Parse with pymupdf4llm Use OCR if needed
    md_text = pymupdf4llm.to_markdown(tmp_path, ocr=True)

    # Log first 1000 characters to console
    # print("=== Parsed Resume Text Preview ===")
    # print(md_text[:1000])
    return clean_markdown(md_text)


def match_resume_with_job(resume_text, job_text):
    resume_doc = nlp(resume_text.lower())
    job_doc = nlp(job_text.lower())

    skills = list(Skill.objects.values_list("name", flat=True))

    matched, missing = [], []
    for skill in skills:
        if skill.lower() in resume_doc.text:
            matched.append(skill)
        elif skill.lower() in job_doc.text:
            missing.append(skill)

    total_required = len(matched) + len(missing)
    match_percentage = (len(matched) / total_required * 100) if total_required > 0 else 0
    summary = f"Resume matches {match_percentage:.2f}% of required skills."

    return match_percentage, matched, missing, summary
