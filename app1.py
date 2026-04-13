import streamlit as st
from resume_parser import parse_resume
from generate_resume import generate_resume

st.title("Resume → Standard Template Converter")

file = st.file_uploader("Upload Resume", type=["pdf","docx"])

if file:

    data = parse_resume(file)

    st.write("Extracted Data")
    st.json(data)

    if st.button("Generate Resume"):

        generate_resume(data)

        with open("converted_resume.docx","rb") as f:
            st.download_button(
                "Download Converted Resume",
                f,
                file_name="standard_resume.docx"
            )
