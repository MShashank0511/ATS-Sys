import streamlit as st
from PIL import Image
import os
import io
import base64
from PyPDF2 import PdfReader
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
# Configure Google Generative AI
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    st.error("API Key for Google Generative AI is missing.")
    st.stop()

genai.configure(api_key=api_key)

def get_gemini_response(input, pdf_content, prompt):
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content([input, pdf_content, prompt])
        return response.text
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return "Error generating response."

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        try:
            reader = PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                text += str(page.extract_text() or '')
            return text
        except Exception as e:
            st.error(f"Error reading PDF file: {e}")
            return ""
    else:
        st.error("No file uploaded")
        return ""

st.set_page_config(page_title="ATS Resume Expert")
st.header("Resume Review System")

jd = st.text_area("Job Description:", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

input_prompt_name = """
Extract the name of the student from the resume text.
"""

input_prompt_college = """
Extract the college of the student from the resume text.
"""

input_prompt_roll_number = """
Extract the roll number of the student from the resume text."""

input_prompt_branch = """
Extract the engineering branch of the student from the resume text."""

input_prompt_cgpa= """
Extract the CGPA or percentage of the student mentioned in the resume text. Just give the number as output."""

input_prompt_interest = """
Identify the area of interest of the student from the resume text based on the projects mentioned or experiences . Possible areas include Frontend, Backend, Data Science, Data Analyst, or core branches roles like process engineeringetc.
"""
input_prompt_rating = """
Evaluate the resume based on the following criteria:
1. Quality of projects and experiences
2. Presentation and formatting
3. Position of responsibilities under taken
Provide a rating out of 10, considering all these aspects.
Provide only the number and no other information.
"""


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")
    
    pdf_content=input_pdf_setup(uploaded_file)
    name_response = get_gemini_response(pdf_content, input_prompt_name,input_prompt_name)
    college_response = get_gemini_response(pdf_content, input_prompt_college,input_prompt_college)
    roll_number_response = get_gemini_response(pdf_content, input_prompt_roll_number,input_prompt_roll_number)
    branch_response = get_gemini_response(pdf_content, input_prompt_branch,input_prompt_branch)
    interest_response = get_gemini_response(pdf_content, input_prompt_interest,input_prompt_interest)
    rating_response = get_gemini_response(pdf_content, input_prompt_rating,input_prompt_rating)
    cgpa_response = get_gemini_response(pdf_content, input_prompt_cgpa,input_prompt_cgpa)
    
    if(len(roll_number_response)>15):
        roll_number_response="NULL"
    if(len(cgpa_response)>15):
        cgpa_response="NULL"

    st.write(f"Name: {name_response.strip()}")
    st.write(f"College: {college_response.strip()}")
    st.write(f"Roll Number: {roll_number_response.strip()}")
    st.write(f"Branch: {branch_response.strip()}")
    st.write(f"Area of Interest: {interest_response.strip()}")
    st.write(f"Rating: {rating_response.strip()}")
    st.write(f"CGPA: {cgpa_response.strip()}")
    


submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("How Can I Improvise my Skills")
submit3 = st.button("Percentage Match")
submit4 = st.button("Resources to Upskill")

input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume. Give a brief introduction 
about the candidate including their name, education, experiences, and skills in one paragraph.
Please share your professional evaluation on whether the candidate's profile is technically strong or not. 
Highlight the strengths and weaknesses of the applicant based on the skills and experiences mentioned in the resume. 
Provide an overall assessment of the candidate's technical proficiency with respect to the job description provided finally.
"""

input_prompt2 = """You are an experienced Career Development Coach. Your task is to review the provided resume against
 the job description. Please share your professional evaluation on how the candidate can further develop their skills
   to better align with the role. Highlight the areas where the candidate shows potential and provide specific 
   recommendations for improvement in relation to the specified job requirements."""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS 
functionality. Your task is to evaluate the resume against the provided job description. Give me the percentage of 
match if the resume matches the job description. First, the output should come as a percentage and then keywords missing
and finally, final thoughts.
"""

input_prompt4 = """
I have a job description and a resume. The job description lists certain 
skills and qualifications required for the position. 
The resume, however, is missing some of these skills. Generate a list of the best online resources 
(such as courses, tutorials, books, or articles) that can help someone acquire the missing skills mentioned in the 
job description. Here are the details:

Job Description:

Required Skill 1
Required Skill 2
Required Skill 3
Required Skill 4

Resume:

Existing Skill A
Existing Skill B
Existing Skill C

Missing Skills:

Required Skill 1
Required Skill 3

Please provide links to the best resources for learning these missing skills.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        if pdf_content:
            response = get_gemini_response(jd, pdf_content, input_prompt1)
            st.subheader("The Response is")
            st.write(response)
    else:
        st.write("Please upload the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        if pdf_content:
            response = get_gemini_response(jd, pdf_content, input_prompt2)
            st.subheader("The Response is")
            st.write(response)

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        if pdf_content:
            response = get_gemini_response(jd, pdf_content, input_prompt3)
            st.subheader("The Response is")
            st.write(response)

elif submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        if pdf_content:
            response = get_gemini_response(jd, pdf_content, input_prompt4)
            st.subheader("The Response is")
            st.write(response)

else:
    st.write("Please upload the resume")


