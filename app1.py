import streamlit as st
import pdfplumber
from docxtpl import DocxTemplate
import google.generativeai as genai
from io import BytesIO

# Configure Gemini API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-pro")

st.title("AI Resume → Template Converter")

uploaded_file = st.file_uploader("Upload Resume", type=["pdf"])


def extract_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


def convert_resume(text):

    prompt = f"""
Convert the following resume into this structure:

Name
Title
Location
Contact
Professional Summary
Key Achievements
Technical Skills
Professional Experience
Education

Resume:
{text}
"""

    response = model.generate_content(prompt)

    return response.text


if uploaded_file:

    text = extract_text(uploaded_file)

    st.success("Resume uploaded successfully!")

    if st.button("Convert Resume"):

        result = convert_resume(text)

        doc = DocxTemplate("template.docx")

        doc.render({
            "content": result
        })

        buffer = BytesIO()

        doc.save(buffer)

        buffer.seek(0)

        st.download_button(
            "Download Converted Resume",
            buffer,
            file_name="converted_resume.docx"
        )
