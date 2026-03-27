import os
import re
import fitz  # PyMuPDF
from db import supabase

RESUME_FOLDER = "incoming_resumes"

COMMON_SKILLS = [
    "python", "java", "c++", "c#", "javascript", "typescript", "sql",
    "aws", "azure", "docker", "kubernetes", "git", "react", "node",
    "linux", "tensorflow", "pytorch", "machine learning", "data analysis",
    "project management", "agile", "scrum", "jira", "excel", "power bi",
    "embedded systems", "defense systems", "cybersecurity", "devops"
]

CLEARANCE_PATTERNS = [
    "ts/sci",
    "top secret",
    "secret clearance",
    "secret",
    "confidential"
]

def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)

    for page in doc:
        page_text = page.get_text()
        if page_text:
            text += page_text + "\n"

    doc.close()
    return text.strip()

def applicant_exists(email):
    response = supabase.table("applicants").select("*").eq("email", email).execute()
    return len(response.data) > 0

def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group(0).strip() if match else None

def extract_phone(text):
    match = re.search(r'(\+?1[-.\s]?)?(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})', text)
    return match.group(0).strip() if match else None

def looks_like_name(line):
    line = line.strip()

    if not line:
        return False

    bad_words = [
        "summary", "education", "experience", "skills", "technical skills",
        "projects", "certifications", "contact", "profile", "objective",
        "work experience", "professional experience"
    ]
    if line.lower() in bad_words:
        return False

    if len(line) > 40:
        return False

    if "@" in line or "linkedin" in line.lower() or re.search(r'\d', line):
        return False

    words = line.replace(",", " ").split()
    if len(words) < 2 or len(words) > 4:
        return False

    for word in words:
        cleaned = re.sub(r"[^A-Za-z\-']", "", word)
        if not cleaned:
            return False

    return True

def extract_name(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    for line in lines[:8]:
        if looks_like_name(line):
            return line.title()

    return None

def extract_skills(text):
    lower = text.lower()
    found = []

    for skill in COMMON_SKILLS:
        if skill in lower:
            found.append(skill.title())

    return sorted(list(set(found)))

def extract_years_experience(text):
    matches = re.findall(r"(\d+)\s*\+?\s*years", text.lower())
    if matches:
        return max(int(x) for x in matches)
    return 0

def extract_clearance(text):
    lower = text.lower()

    if "ts/sci" in lower:
        return "TS/SCI"
    if "top secret" in lower:
        return "Top Secret"
    if "secret clearance" in lower:
        return "Secret"
    if re.search(r"\bsecret\b", lower):
        return "Secret"
    if "confidential" in lower:
        return "Confidential"

    return None

def guess_name_from_filename(filename):
    name = os.path.splitext(filename)[0]
    name = name.replace("_", " ").replace("-", " ").strip()
    return name.title()

def guess_email_from_name(name):
    base = name.lower().replace(" ", ".")
    return f"{base}@unknown.com"

def parse_resume(resume_text, filename):
    extracted_name = extract_name(resume_text)
    extracted_email = extract_email(resume_text)
    extracted_phone = extract_phone(resume_text)
    extracted_skills = extract_skills(resume_text)
    extracted_years = extract_years_experience(resume_text)
    extracted_clearance = extract_clearance(resume_text)

    full_name = extracted_name if extracted_name else guess_name_from_filename(filename)
    email = extracted_email if extracted_email else guess_email_from_name(full_name)

    parsed = {
        "full_name": full_name,
        "email": email,
        "phone": extracted_phone,
        "skills": extracted_skills,
        "years_experience": extracted_years,
        "clearance": extracted_clearance
    }

    return parsed

def import_pdfs(company_id=1, job_opening_id=1):
    if not os.path.exists(RESUME_FOLDER):
        return {
            "imported": 0,
            "skipped": 0,
            "message": "Resume folder not found."
        }

    files = [f for f in os.listdir(RESUME_FOLDER) if f.lower().endswith(".pdf")]

    imported = 0
    skipped = 0

    for filename in files:
        pdf_path = os.path.join(RESUME_FOLDER, filename)
        resume_text = extract_text_from_pdf(pdf_path)

        parsed = parse_resume(resume_text, filename)

        if applicant_exists(parsed["email"]):
            skipped += 1
            continue

        payload = {
            "company_id": company_id,
            "job_opening_id": job_opening_id,
            "full_name": parsed["full_name"],
            "email": parsed["email"],
            "phone": parsed["phone"],
            "resume_text": resume_text,
            "parsed_resume_json": parsed
        }

        supabase.table("applicants").insert(payload).execute()
        imported += 1

    return {
        "imported": imported,
        "skipped": skipped,
        "message": f"Processed {len(files)} PDF file(s)."
    }

if __name__ == "__main__":
    result = import_pdfs()
    print(result)