from docxtpl import DocxTemplate

def generate_resume(data):

    doc = DocxTemplate("sample_template.docx")

    context = {
        "name": data["name"],
        "email": data["email"],
        "phone": data["phone"],
        "summary": data["summary"],
        "skills": data["skills"],
        "experience": data["experience"],
        "education": data["education"]
    }

    doc.render(context)
    doc.save("converted_resume.docx")
