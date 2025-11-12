from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert the pdf to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        poppler_path=r"C:\Users\Lenovo\Downloads\Release-23.08.0-0\poppler-23.08.0\Library\bin"

load_dotenv()

import streamlit as st
import os, io, base64, pdf2image, google.generativeai as genai
from PIL import Image
from PyPDF2 import PdfReader

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
POPPLER_BIN = r"C:\Users\Lenovo\Downloads\Release-23.08.0-0\poppler-23.08.0\Library\bin"

def choose_model(prefer_vision=True):
    try:
        models = list(genai.list_models())
        for m in models:
            name = getattr(m, "name", "")
            methods = getattr(m, "supported_generation_methods", [])
            if "generateContent" in methods:
                if prefer_vision and any(k in name.lower() for k in ("vision", "pro-vision")):
                    return name
        for m in models:
            if "generateContent" in getattr(m, "supported_generation_methods", []):
                return m.name
    except:
        return "gemini-1.5-flash"
    return "gemini-1.5-flash"

def input_pdf_setup(uploaded_file):
    uploaded_file.seek(0)
    content_bytes = uploaded_file.read()
    pdf_parts = []
    try:
        images = pdf2image.convert_from_bytes(content_bytes, poppler_path=POPPLER_BIN)
        for img in images[:3]:
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            pdf_parts.append({
                "mime_type": "image/png",
                "data": base64.b64encode(buf.getvalue()).decode("utf-8")
            })
    except:
        pass
    text = ""
    try:
        reader = PdfReader(io.BytesIO(content_bytes))
        text = "\n".join(p.extract_text() or "" for p in reader.pages)
    except:
        pass
    return pdf_parts, text

def get_gemini_response(input_prompt, pdf_parts, job_desc):
    model_name = choose_model(True)
    try:
        model = genai.GenerativeModel(model_name)
        if pdf_parts:
            response = model.generate_content([input_prompt, pdf_parts[0], job_desc])
        else:
            response = model.generate_content([input_prompt, job_desc])
        return response.text
    except:
        model = genai.GenerativeModel(choose_model(False))
        response = model.generate_content([input_prompt, job_desc])
        return response.text

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

input_text = st.text_area("Job Description:", key="input")


submit1 = st.button("Tell me About the resume")
submit2 = st.button("How can I improve my Skills")
submit3 = st.button("percentage match")

input_prompt1 = """ You are an experienced HR professional with technical expertise in Data Science, Full-Stack Web Development, and Big Data Engineering, devops.
Your task is to review the provided resume against the job description for these profiles.
Please provide a comprehensive professional evaluation on whether the candidate’s profile aligns with the job requirements.
Highlight the strengths and weaknesses of the applicant in relation to the specified criteria.."""

input_prompt2 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of job matching. 
Your task is to evaluate the resume against the provided job description. 
Give a detailed analysis of how well the resume matches the job description. 
First, the output should come as a percentage match, and then list key strengths and missing keywords or skills.
"""

def input_pdf_setup(uploaded_file):
    if uploaded_file is None:
        raise FileNotFoundError("No PDF file uploaded.")

    uploaded_file.seek(0)
    content_bytes = uploaded_file.read()
    pdf_parts = []
    try:
        images = pdf2image.convert_from_bytes(
            content_bytes,
            poppler_path=r"C:\Users\Lenovo\Downloads\Release-23.08.0-0\poppler-23.08.0\Library\bin"
        )
        first_page = images[0]
        buf = io.BytesIO()
        first_page.save(buf, format="PNG")
        pdf_parts = [{
            "mime_type": "image/png",
            "data": base64.b64encode(buf.getvalue()).decode("utf-8")
        }]
    except Exception:
        pdf_parts = []

    text = ""
    try:
        reader = PdfReader(io.BytesIO(content_bytes))
        text = "\n".join(p.extract_text() or "" for p in reader.pages)
    except Exception:
        text = ""

    return pdf_parts, text

            

## Streamlit App
st.set_page_config(page_title="ATS Resume Expert")

# buttons with unique keys
col1, col2, col3 = st.columns(3)
submit1 = col1.button("Tell me About the resume", key="btn_about")
submit2 = col2.button("How can I improve my Skills", key="btn_improve")
submit3 = col3.button("percentage match", key="btn_percent")


input_prompt1 = """ You are an experienced HR professional with technical expertise in Data Science, Full-Stack Web Development, and Big Data Engineering, devops.
Your task is to review the provided resume against the job description for these profiles.
Please provide a comprehensive professional evaluation on whether the candidate’s profile aligns with the job requirements.
Highlight the strengths and weaknesses of the applicant in relation to the specified criteria.."""

input_prompt2 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of job matching. 
Your task is to evaluate the resume against the provided job description. 
Give a detailed analysis of how well the resume matches the job description. 
First, the output should come as a percentage match, and then list key strengths and missing keywords or skills.
"""
if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Reponses is")
        st.write(response)

    else:
        st.write("Please upload a resume")
elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("The Reponses is")
        st.write(response)
    else:
        st.write("Please upload a resume")
        