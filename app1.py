import streamlit as st
import pdfplumber
from docxtpl import DocxTemplate
import google.generativeai as genai
from io import BytesIO

# Configure Gemini API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Correct Gemini model
model = genai.GenerativeModel("gemini-1.5-flash-latest")

st.title("AI Resume → Template Converter")

uploaded_file = st.file_uploader("Upload Resume", type=["pdf"])


# Extract text from PDF
def extract_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


# Convert resume using Gemini
def convert_resume(text):

    # limit size to avoid API errors
    text = text[:6000]

    prompt = f"""
Extract and rewrite the following resume into this structured format.

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

            doc.render({
                "content": result
            })

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
