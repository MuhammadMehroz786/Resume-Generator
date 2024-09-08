# This is app is currently deployed as mvp on Streamlit sharing. The app is a resume to job description matching scorer that allows users to compare their resume against a job description to gauge the match quality. The app provides a matching score and an interpretation of the score, such as "Excellent Match" or "Poor Match." Users can paste their resume and job description text or upload DOCX/PDF files for comparison. The app also includes a feedback form for users to share their thoughts and suggestions.

import streamlit as st
from processing import document_cleaner, keyword_extractor_nltk
from processing.keyword_extractor_nltk import extract_keywords
from processing.matcher_nltk import get_text_from_docx, get_text_from_pdf

# Define service functions
def resume_and_job_description_keyword_matcher():
    st.subheader("Resume Keyword Search Optimization")
    resume_text = get_input_text("Resume")
    job_description_text = get_input_text("Job Description")
    
    # Submit button to trigger keyword matching
    if st.button('Match Keywords'):
        if resume_text and job_description_text:
            resume_keywords = extract_keywords(resume_text)
            job_description_keywords = extract_keywords(job_description_text)
            st.write("Matching Keywords from Resume to Job Description")
            st.write("Resume Keywords:", resume_keywords)
            st.write("Job Description Keywords:", job_description_keywords)
        else:
            st.error("Please provide both resume and job description texts.")

# Function to handle text input or file upload and return text
def get_input_text(title):
    text_input = st.text_area(f"Paste your {title} text here or upload a {title} file:")
    file = st.file_uploader(f"Or upload a DOCX/PDF file for your {title}:", type=['docx', 'pdf'])
    if text_input:
        return text_input
    elif file:
        if file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return get_text_from_docx(file)
        elif file.type == "application/pdf":
            return get_text_from_pdf(file)
    return None

# Sidebar for navigation with dropdown for other pages
st.sidebar.title("Career Navigation")
menu_option = st.sidebar.selectbox("Menu", ["Services", "User Feedback"])

if menu_option == "Services":
    st.header("Resume and Job Description Keyword Matcher")
    resume_and_job_description_keyword_matcher()
    st.write("Disclaimer: This is an AI-assisted keyword matcher and may make mistakes. Users are responsible for verification and validation of the information provided.")

elif menu_option == "User Feedback":
    st.header("User Feedback Form")
    st.write("Your feedback is valuable to us. Please share your thoughts and suggestions.")
    feedback = st.text_area("Feedback")
    if st.button("Submit Feedback"):
        st.success("Thank you for your feedback! We appreciate your time.")
        # Here you might want to handle the feedback, e.g., saving it somewhere

# Define the function used in the Services section
def resume_and_job_description_keyword_matcher():
    # Assume some functionality here that processes input and shows outputs
    st.write("Keyword matching functionality not implemented in this snippet.")

# Main function to run the Streamlit app
def main():
    if menu_option == "Services":
        st.header("Keyword Matcher")
        st.write("Use this tool to find how well your resume matches up with job descriptions.")
        resume_and_job_description_keyword_matcher()

# Check if the script is run as the main program and launch Streamlit app
if __name__ == "__main__":
    main()