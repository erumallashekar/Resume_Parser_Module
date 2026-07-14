# 📄 Resume Parser

A Python/Django-based tool for extracting structured information from resumes.  
The parser supports multiple formats (PDF, DOCX, TXT) and converts unstructured resume text into machine-readable data such as name, email, phone number, skills, education, and work experience.

---

## 🚀 Features
- Parse resumes in **PDF, DOCX, and TXT** formats
- Extract key fields:
  - Contact information (name, email, phone)
  - Education details
  - Work experience
  - Skills and certifications
- JSON output for easy integration with other systems
- Modular design for extending with custom fields
- Django REST API endpoints for uploading and parsing resumes

---

## 🛠️ Tech Stack
- **Python 3.10+**
- **Django / Django REST Framework**
- **NLTK / spaCy** for NLP
- **PyPDF2 / python-docx** for file parsing

---

## 📦 Installation

Clone the repository:
```bash
git clone https://github.com/your-username/resume-parser.git
cd resume-parser
