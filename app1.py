import streamlit as st
import pdfplumber
from docxtpl import DocxTemplate
from openai import OpenAI
from io import BytesIO
st.write("Key loaded:", bool(st.secrets.get("OPENAI_API_KEY")))
# Configure OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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


# Convert resume using OpenAI
def convert_resume(text):

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

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


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
