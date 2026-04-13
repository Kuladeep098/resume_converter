import pdfplumber
from docx import Document
import re
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_text(file):

    if file.name.endswith(".pdf"):
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
        return text

    elif file.name.endswith(".docx"):
        doc = Document(file)
        return "\n".join([p.text for p in doc.paragraphs])

    return ""


def extract_name(text):
    doc = nlp(text[:1000])
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return ""


def extract_email(text):
    match = re.search(r'\S+@\S+', text)
    return match.group(0) if match else ""


def extract_phone(text):
    match = re.search(r'\+?\d[\d\s\-]{8,15}', text)
    return match.group(0) if match else ""


def extract_summary(text):

    patterns = [
        "PROFESSIONAL SUMMARY",
        "SUMMARY",
        "CAREER OBJECTIVE",
        "OBJECTIVE"
    ]

    for p in patterns:
        match = re.search(p + r"(.*?)(SKILLS|EXPERIENCE|PROJECT)", text, re.S | re.I)
        if match:
            return match.group(1).strip()

    return ""


def extract_skills(text):

    skill_keywords = [
        "Java","Python","SQL","Spring Boot","Microservices",
        "Selenium","Jenkins","Docker","REST","API",
        "Manual Testing","Automation Testing","JIRA",
        "MySQL","Postman","Git","Maven","Hibernate"
    ]

    found = []

    for skill in skill_keywords:
        if skill.lower() in text.lower():
            found.append(skill)

    return ", ".join(found)


def extract_experience(text):

    match = re.search(
        r"(PROFESSIONAL EXPERIENCE|EMPLOYMENT DETAILS)(.*?)(EDUCATION)",
        text,
        re.S | re.I
    )

    if match:
        return match.group(2)

    return ""


def extract_education(text):

    match = re.search(r"(EDUCATION.*)", text, re.S | re.I)

    if match:
        return match.group(1)

    return ""


def parse_resume(file):

    text = extract_text(file)

    data = {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "summary": extract_summary(text),
        "skills": extract_skills(text),
        "experience": extract_experience(text),
        "education": extract_education(text)
    }

    return data
