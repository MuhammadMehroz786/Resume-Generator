# This is app is currently deployed as mvp on Streamlit sharing. The app is a resume to job description matching scorer that allows users to compare their resume against a job description to gauge the match quality. The app provides a matching score and an interpretation of the score, such as "Excellent Match" or "Poor Match." Users can paste their resume and job description text or upload DOCX/PDF files for comparison. The app also includes a feedback form for users to share their thoughts and suggestions.

import streamlit as st
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import pandas as pd
import matplotlib.pyplot as plt
import docx  # Import for working with DOCX files
import fitz  # Import for working with PDF files (PyMuPDF)

# Ensure NLTK resources are downloaded
nltk.download('punkt')
nltk.download('stopwords')

def get_text_from_docx(file):
    """
    Extracts text from a DOCX file.
    """
    doc = docx.Document(file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def get_text_from_pdf(file):
    """
    Extracts text from a PDF file.
    """
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    text = ''
    for page in pdf:
        text += page.get_text()
    return text

# Define service functions
def resume_improvement_generator():
    st.subheader("Resume and Job Description Documents Analysis and Matching App")
    resume_text = get_input_text("Resume")
    job_description_text = get_input_text("Job Description")
    
    if st.button('Generate Improved Resume'):
        if resume_text and job_description_text:
            resume_keywords = extract_keywords(resume_text)
            job_desc_keywords = extract_keywords(job_description_text)
            suggestions = suggest_sentence_improvements(resume_text, job_description_text, resume_keywords, job_desc_keywords)
            
            if suggestions:
                st.write("Here are some suggestions to improve your resume based on the job description:")
                for suggestion in suggestions:
                    st.write(f"- {suggestion}")
            else:
                st.write("Your resume is well-aligned with the job description.")
        else:
            st.error("Please provide both resume and job description texts.")

def extract_keywords(text):
    words = word_tokenize(text.lower())
    stop_words_set = set(stopwords.words('english'))
    keywords = [word for word in words if word.isalnum() and word not in stop_words_set]
    return keywords

def suggest_sentence_improvements(resume_text, job_description_text, resume_keywords, job_desc_keywords):
    sentences_resume = sent_tokenize(resume_text)
    suggestions = []

    # Find keywords in job description not mentioned in the resume
    missing_keywords = [kw for kw in job_desc_keywords if kw not in resume_keywords]
    if missing_keywords:
        suggestions.append(f"Consider adding these skills/qualifications from the job description to your resume: {', '.join(missing_keywords)}")

    # Suggest improvements based on sentence analysis
    for sent in sentences_resume:
        words = word_tokenize(sent)
        if len(words) > 25:  # Threshold for sentence length can be adjusted
            suggestions.append(f"Consider breaking down long sentences for clarity: '{sent[:50]}...'")

    return suggestions

def get_input_text(doc_type):
    text_input = st.text_area(f"Paste your {doc_type} text here or upload a {doc_type} file:")
    file = st.file_uploader(f"Or upload a DOCX/PDF file for your {doc_type}:", type=['docx', 'pdf'])
    if text_input:
        return text_input
    elif file:
        if file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            # Implement get_text_from_docx using python-docx or similar library
            return get_text_from_docx(file)
        elif file.type == "application/pdf":
            # Implement get_text_from_pdf using PyMuPDF (fitz) or similar library
            return get_text_from_pdf(file)
    return None

# Main page setup
st.sidebar.title("Career Navigation")
page = st.sidebar.radio("Go to", ["Services", "User Feedback"])

if page == "Services":
    st.header("Resume Improvement Generator")
    st.write("Harness the power of AI to enhance your resume and job matching experience.")
    resume_improvement_generator()
    st.write("Disclaimer: This is an AI-assisted resume matcher and may make mistakes. Users are responsible for verification and validation of the information provided.")

elif page == "User Feedback":
    st.header("User Feedback Form")
    st.write("We value your feedback and use it to improve our service. Please share your thoughts and suggestions below.")
    
    # Creating a simple feedback form
    with st.form(key='feedback_form'):
        feedback_text = st.text_area("Enter your feedback here:")
        feedback_rating = st.select_slider("Rate our service:", options=['Poor', 'Fair', 'Good', 'Very Good', 'Excellent'])
        submit_button = st.form_submit_button("Submit Feedback")
    
    if submit_button:
        st.success("Thank you for your feedback!")
        # Here you could also include code to save the feedback to a database or file

    st.write("Disclaimer: Our support team is here to help, but users should verify information received from support for accuracy.")
