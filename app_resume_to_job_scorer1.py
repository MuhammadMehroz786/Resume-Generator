import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from processing import document_cleaner, keyword_extractor
from processing.keyword_extractor import extract_keywords
from optimization.formatting_recommendations import suggest_resume_formatting
from optimization.sentence_reconstruction import suggest_sentence_improvements
from processing.matcher import calculate_matching_scores, get_text_from_docx, get_text_from_pdf

# Additional function for career stage specific interpretation
def interpret_score_with_career_stage(score, career_stage):
    if score >= 0.8:
        feedback = "Excellent Match: This score indicates a strong alignment. "
    elif score >= 0.6:
        feedback = "Good Match: Indicates a resume that aligns well with the job requirements. "
    elif score >= 0.4:
        feedback = "Fair Match: Suggests some alignment but indicates the need for better highlighting. "
    else:
        feedback = "Poor Match: Indicates a significant misalignment. "
    
    if career_stage == "Recent Graduates":
        feedback += "As a recent graduate, focus on highlighting coursework, projects, and skills relevant to the job."
    elif career_stage == "Mid-Career Professionals":
        feedback += "As a mid-career professional, ensure to highlight your relevant experiences and achievements."
    elif career_stage == "Career Transition":
        feedback += "In career transition, emphasize transferable skills and relevant experiences for the new field."
    
    return feedback

# Sidebar for navigation and career stage selection
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Services"])
career_stage = st.sidebar.selectbox("Select Your Career Stage", ["Recent Graduates", "Mid-Career Professionals", "Career Transition"])

# Function modifications to use the enhanced interpret_score_with_career_stage function
def resume_to_job_description_matching_scorer():
    st.subheader("Resume to Job Description Matching Scorer")
    resume_text = get_input_text("resume")
    job_description_text = get_input_text("job description")
    if resume_text and job_description_text:
        score = calculate_matching_scores(resume_text, job_description_text)
        interpretation = interpret_score_with_career_stage(score, career_stage)
        st.write(f"Matching Score: {score:.2f} - {interpretation}")

# Include other function definitions here as in the original script

# Page Content based on navigation
if page == "Home":
    st.header("Welcome to the Document Analysis and Matching App")
    # Home page content here

elif page == "Services":
    st.header("Services")
    # Services page content and function calls here

    if service == "Resume and Job Description Keyword Matcher":
        resume_and_job_description_keyword_matcher()
    elif service == "Resume to Job Description Matching Scorer":
        resume_to_job_description_matching_scorer()
    # Include other services as needed
