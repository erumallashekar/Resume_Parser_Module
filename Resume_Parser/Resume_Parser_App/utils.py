import pdfplumber
import docx
import spacy
import re
from pathlib import Path

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    nlp = spacy.blank("en")

SECTION_HEADERS = {
    "summary": ["summary", "professional summary", "about me", "profile", "career summary", "summary statement"],
    "skills": ["skills", "technical skills", "skill set", "core skills"],
    "education": ["education", "academic qualifications", "education & training", "educational background"],
    "experience": ["experience", "work experience", "professional experience", "employment history", "workexperience", "professionalexperience"],
    "projects": ["projects", "project experience", "project details"],
    "certifications": ["certifications", "certification", "licenses", "certifications & licenses"],
    "languages": ["languages", "language skills", "language"],
}

HEADER_PATTERN = re.compile(r"^[A-Za-z ]{2,100}$")


def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()


def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs]).strip()


def extract_text_from_txt(file_path):
    return Path(file_path).read_text(encoding="utf-8").strip()


def normalize_section_name(line):
    normalized = line.strip().lower().replace("\r", "")
    normalized = re.sub(r"[^a-z0-9 ]+", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()

    for key, names in SECTION_HEADERS.items():
        for name in names:
            normalized_name = re.sub(r"[^a-z0-9 ]+", " ", name.lower()).strip()
            if normalized == normalized_name:
                return key
            if re.search(r"\b" + re.escape(normalized_name) + r"\b", normalized):
                return key

    for key in SECTION_HEADERS:
        if re.search(r"\b" + re.escape(key) + r"\b", normalized):
            return key

    return None


def split_into_sections(text):
    sections = {key: [] for key in SECTION_HEADERS}
    current_section = None
    lines = [line.rstrip() for line in text.splitlines()]

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        section_key = normalize_section_name(stripped)
        if section_key:
            current_section = section_key
            continue

        if current_section:
            sections[current_section].append(stripped)
        else:
            sections.setdefault("header", []).append(stripped)

    return sections


def extract_name(text, sections):
    header_lines = sections.get("header", [])
    for line in header_lines[:4]:
        if line.lower().startswith("name:"):
            return line.split(":", 1)[1].strip()
    if header_lines:
        first = header_lines[0].strip()
        if ":" not in first and len(first.split()) <= 5:
            return first

    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text

    return ""


def extract_address(sections):
    header_lines = sections.get("header", [])
    for line in header_lines[:8]:
        if line.lower().startswith("address:"):
            return line.split(":", 1)[1].strip()

    address_lines = []
    capture = False
    for line in header_lines:
        if line.lower().startswith("address:"):
            capture = True
            address_lines.append(line.split(":", 1)[1].strip())
        elif capture and line and ":" not in line:
            address_lines.append(line.strip())
        elif capture:
            break

    return " ".join(address_lines).strip()


def split_into_blocks(lines):
    blocks = []
    current = []
    for line in lines:
        if not line.strip():
            if current:
                blocks.append(current)
                current = []
        else:
            current.append(line.strip())
    if current:
        blocks.append(current)
    return blocks


def parse_list_section(lines):
    return [line.strip() for line in lines if line.strip()]


def parse_education_section(lines):
    blocks = split_into_blocks(lines)
    items = []
    for block in blocks:
        text = " ".join(block)
        years = re.search(r"(\d{4})\s*[-–]\s*(\d{4}|present|Present)", text)
        start_year = years.group(1) if years else ""
        end_year = years.group(2) if years else ""
        institution = block[0] if block else ""
        degree = ""
        if len(block) > 1:
            candidate = block[1]
            if any(word in candidate.lower() for word in ["bachelor", "master", "phd", "degree", "diploma"]):
                degree = candidate
            elif any(word in institution.lower() for word in ["university", "college", "institute"]):
                institution = block[1]
                degree = block[0]
        items.append({
            "institution": institution,
            "degree": degree,
            "start_year": start_year,
            "end_year": end_year,
        })
    return items


def parse_experience_section(lines):
    blocks = split_into_blocks(lines)
    items = []
    for block in blocks:
        title = block[0] if block else ""
        company = block[1] if len(block) > 1 else ""
        dates = "".join(block[2:3]) if len(block) > 2 else ""
        year_match = re.search(r"(\d{4})\s*[-–]\s*(\d{4}|present|Present)", " ".join(block))
        start_date = year_match.group(1) if year_match else ""
        end_date = year_match.group(2) if year_match else ""
        description = " ".join(block[2:]) if len(block) > 2 else ""
        if not company and len(block) > 2:
            company = block[2]
            description = " ".join(block[3:])
        items.append({
            "company": company,
            "role": title,
            "start_date": start_date,
            "end_date": end_date,
            "description": description,
        })
    return items


def parse_project_section(lines):
    blocks = split_into_blocks(lines)
    items = []
    for block in blocks:
        title = block[0] if block else ""
        description = " ".join(block[1:]) if len(block) > 1 else ""
        items.append({"title": title, "description": description})
    return items


def parse_certification_section(lines):
    return [line.strip() for line in lines if line.strip()]


def parse_language_section(lines):
    return [line.strip() for line in lines if line.strip()]


def find_certifications_in_text(text):
    certifications = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if re.search(r"\b(certification|certifications|certificate|certified)\b", stripped, re.IGNORECASE):
            if stripped.lower() not in ("certification", "certifications", "certificate", "certified"):
                certifications.append(stripped)

    # If the text contains a certifications section header but no items, capture following lines
    match = re.search(r"(?i)(certifications|certification|licenses|certificate)\s*[:\r\n]+([\s\S]+?)(?:\n\n|$)", text)
    if match:
        section_text = match.group(2).strip()
        if section_text:
            for line in section_text.splitlines():
                stripped = line.strip()
                if stripped and stripped.lower() not in ("certification", "certifications", "certificate", "certified"):
                    if stripped not in certifications:
                        certifications.append(stripped)

    return certifications


def parse_resume(file_path):
    file_path = str(file_path)
    if file_path.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        text = extract_text_from_docx(file_path)
    elif file_path.endswith(".txt"):
        text = extract_text_from_txt(file_path)
    else:
        return {}

    if not text:
        return {}

    sections = split_into_sections(text)
    header_text = "\n".join(sections.get("header", []))
    name = extract_name(text, sections)

    email_match = re.search(r"[\w\.-]+@[\w\.-]+", text)
    phone_match = re.search(r"\+?\d[\d\s()-]{7,}\d", text)

    email = email_match.group(0) if email_match else ""
    phone = phone_match.group(0).strip() if phone_match else ""
    address = extract_address(sections)

    skills = parse_list_section(sections.get("skills", []))
    education = parse_education_section(sections.get("education", []))
    experience = parse_experience_section(sections.get("experience", []))
    projects = parse_project_section(sections.get("projects", []))
    certifications = parse_certification_section(sections.get("certifications", []))
    if not certifications:
        certifications = find_certifications_in_text(text)
    languages = parse_language_section(sections.get("languages", []))

    summary = "\n".join(sections.get("summary", []))
    if not summary:
        summary = header_text[:500]

    if not name and header_text:
        name = header_text.splitlines()[0].strip()

    if not name and nlp:
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                name = ent.text
                break

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "address": address,
        "skills": skills,
        "education": education,
        "experience": experience,
        "projects": projects,
        "certifications": certifications,
        "languages": languages,
        "summary": summary,
    }
