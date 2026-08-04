import spacy
from .models import Skill, JobDescription
import pymupdf4llm
import tempfile
import fitz  # PyMuPDF
import re
import threading
from .models import ResumeDownloadHistory


nlp = spacy.load("en_core_web_sm")

def clean_markdown(md_text):
    return re.sub(r'[#\-\*`]', '', md_text)

# Global lock to prevent concurrent OCR calls
ocr_lock = threading.Lock()

def extract_text_from_pdf(uploaded_file):
    """
    Safely extract text from a PDF uploaded via Django.
    Handles both text-based and scanned PDFs.
    """
    # Write uploaded file to a temporary path
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        for chunk in uploaded_file.chunks():
            tmp.write(chunk)
        tmp_path = tmp.name

    # First try without OCR (fast for text-based PDFs)
    try:
        md_text = pymupdf4llm.to_markdown(tmp_path, ocr=False)
        if md_text.strip():
            return md_text
    except Exception as e:
        print("Non-OCR extraction failed:", e)

    # Fallback: OCR with lock (for scanned PDFs)
    with ocr_lock:
        md_text = pymupdf4llm.to_markdown(tmp_path, ocr=True)

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

def recommend_jobs(resume_text):
    """
    Simple baseline: recommend jobs based on skill overlap.
    Returns a list of (job, score).
    """
    jobs = JobDescription.objects.all()
    recommendations = []

    resume_words = set(resume_text.lower().split())

    for job in jobs:
        job_words = set(job.description.lower().split())
        overlap = resume_words.intersection(job_words)
        score = len(overlap) / max(len(job_words), 1)
        recommendations.append((job, score))

    # Sort by score descending
    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations[:5]  # top 5 jobs
    

def record_download(resume, version="v1"):
    ResumeDownloadHistory.objects.create(resume=resume, version=version)
