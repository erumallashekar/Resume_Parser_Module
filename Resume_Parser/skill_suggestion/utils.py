import spacy
from PyPDF2 import PdfReader
from .models import Skill

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file_obj):
    reader = PdfReader(file_obj)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + " "
    return text

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
