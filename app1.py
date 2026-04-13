import streamlit as st
import pdfplumber
from docxtpl import DocxTemplate
from openai import OpenAI
from io import BytesIO

client = OpenAI(api_key=st.secrets["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"])

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

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role":"user","content":prompt}]
    )

    return response.choices[0].message.content


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
