# This is app is currently deployed as mvp on Streamlit sharing. The app is a resume to job description matching scorer that allows users to compare their resume against a job description to gauge the match quality. The app provides a matching score and an interpretation of the score, such as "Excellent Match" or "Poor Match." Users can paste their resume and job description text or upload DOCX/PDF files for comparison. The app also includes a feedback form for users to share their thoughts and suggestions.

import streamlit as st
from processing import document_cleaner, keyword_extractor_nltk
from processing.keyword_extractor_nltk import extract_keywords
from optimization.formatting_recommendations_nltk import suggest_resume_formatting, identify_sections, suggest_structure_improvements
from optimization.sentence_reconstruction_nltk import analyze_sentence_complexity, suggest_sentence_improvements
from processing.matcher_nltk import get_text_from_docx, get_text_from_pdf
import pandas as pd
import matplotlib.pyplot as plt

def resume_reformatting_generator():
    st.subheader("Resume Optimization")
    resume_text = get_input_text("your resume")
    # Submit button to trigger reformatting suggestions
    if st.button('Submit for Reformatting Suggestions'):
        if resume_text:
            formatting_suggestions = suggest_resume_formatting(resume_text)
            if formatting_suggestions:
                st.write("Reformatting Suggestions:")
                for suggestion in formatting_suggestions:
                    st.write(f"- {suggestion}")
            else:
                st.write("Your resume formatting looks good. No major changes needed.")
        else:
            st.error("Please upload your resume for reformatting suggestions.")

def get_input_text(title):
    text_input = st.text_area(f"Paste {title} text here or upload a file:")
    file = st.file_uploader(f"Or upload a DOCX/PDF file:", type=['docx', 'pdf'])
    if text_input:
        return text_input
    elif file:
        if file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return get_text_from_docx(file)
        elif file.type == "application/pdf":
            return get_text_from_pdf(file)
    return None


# Main navigation setup with dropdown for additional pages
st.sidebar.title("Career Navigation")
menu_option = st.sidebar.selectbox("Menu", ["Resume Reformatting Generator", "User Feedback"])

if menu_option == "Resume Reformatting Generator":
    st.header("Resume Reformatting Generator")
    resume_reformatting_generator()
    st.write("Disclaimer: This is an AI-assisted service and may make mistakes. Users are responsible for verification and validation of the information provided.")

elif menu_option == "User Feedback":
    st.header("User Feedback Form")
    st.write("Your feedback is valuable to us. Please share your thoughts and suggestions.")
    feedback_text = st.text_area("Feedback")
    feedback_rating = st.slider("How would you rate our service?", 1, 5, 3)
    if st.button("Submit Feedback"):
        st.success("Thank you for your feedback! We appreciate your time and input.")
        # Here you might want to handle the feedback, e.g., saving it somewhere

# Define the function used in the Services section
def resume_reformatting_generator():
    # Assume some functionality here that processes input and shows outputs
    st.write("")

# Main function to run the Streamlit app
def main():
    if menu_option == "Resume Reformatting Generator":
        st.header("Enhance Your Resume")
        st.write("Use this tool to improve your resume's layout and structure for better job matching.")
        resume_reformatting_generator()

# Check if the script is run as the main program and launch Streamlit app
if __name__ == "__main__":
    main()
