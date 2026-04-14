import streamlit as st
import pdfplumber
from docxtpl import DocxTemplate
import google.generativeai as genai
from io import BytesIO

# Load Gemini API key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Recommended Gemini model
model = genai.GenerativeModel("models/gemini-1.5-flash")

st.title("AI Resume → Template Converter")

uploaded_file = st.file_uploader("Upload Resume", type=["pdf"])


def extract_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def convert_resume(text):

    text = text[:6000]

    prompt = f"""
Convert this resume into the following structured format.

Name:
Title:
Location:
Contact:
Professional Summary:
Key Achievements:
Technical Skills:
Professional Experience:
Education:

Resume text:
{text}
"""

    response = model.generate_content(prompt)

    return response.text


if uploaded_file:

    text = extract_text(uploaded_file)

    st.success("Resume uploaded successfully!")

    if st.button("Convert Resume"):

        try:
            result = convert_resume(text)

            doc = DocxTemplate("template.docx")

            doc.render({"content": result})

            buffer = BytesIO()

            doc.save(buffer)
            buffer.seek(0)

            st.download_button(
                "Download Converted Resume",
                buffer,
                file_name="converted_resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

        except Exception as e:
            st.error("Error converting resume")
            st.write(e)
