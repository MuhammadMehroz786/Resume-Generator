import streamlit as st
from processing import document_cleaner, keyword_extractor
from processing.keyword_extractor import extract_keywords
from optimization.formatting_recommendations import suggest_resume_formatting, identify_sections, suggest_structure_improvements
from optimization.sentence_reconstruction import suggest_sentence_improvements
from processing.matcher import calculate_matching_scores, get_text_from_docx, get_text_from_pdf
import pandas as pd
import matplotlib.pyplot as plt

import spacy
from spacy.cli import download

MODEL_NAME = "en_core_web_sm"

# Function to safely load the spaCy model, installing if necessary
def load_spacy_model(model_name):
    try:
        return spacy.load(model_name)
    except IOError:
        print(f"Model {model_name} not found, downloading...")
        download(model_name)
        return spacy.load(model_name)

# Use the function to load your spaCy model
nlp = load_spacy_model(MODEL_NAME)



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

def get_input_text(doc_type):
    text_input = st.text_area(f"Paste your {doc_type} text here or upload a {doc_type} file:")
    file = st.file_uploader(f"Or upload a DOCX/PDF file for your {doc_type}:", type=['docx', 'pdf'])
    if text_input:
        return text_input
    elif file:
        if file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return get_text_from_docx(file)
        elif file.type == "application/pdf":
            return get_text_from_pdf(file)
    return None

# Main page setup
st.sidebar.title("Career Navigation")
page = st.sidebar.radio("Go to", ["Services", "More"])

if page == "Services":
    st.header("Resume Improvement Generator")
    st.write("Harness the power of AI to enhance your resume and job matching experience.")
    resume_improvement_generator()
    st.write("Disclaimer: This is an AI-assisted resume matcher and may make mistakes. Users are responsible for verification and validation of the information provided.")

elif page == "More":
    page_options = st.sidebar.selectbox("Explore More", ["Home", "User Feedback"])

    if page_options == "Home":
        st.header("Welcome to the Resume Improvement Generator App")
        st.write("Optimize your resume with our AI-driven insights for a competitive edge in the job market.")

    elif page_options == "User Feedback":
        st.header("User Feedback Form")
        st.write("Your feedback is valuable to us. Please share your thoughts and suggestions.")
        st.write("Disclaimer: Our support team is here to help, but users should verify information received from support for accuracy.")
