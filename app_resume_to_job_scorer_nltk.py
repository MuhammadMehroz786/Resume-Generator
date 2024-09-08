# This is app is currently deployed as mvp on Streamlit sharing. The app is a resume to job description matching scorer that allows users to compare their resume against a job description to gauge the match quality. The app provides a matching score and an interpretation of the score, such as "Excellent Match" or "Poor Match." Users can paste their resume and job description text or upload DOCX/PDF files for comparison. The app also includes a feedback form for users to share their thoughts and suggestions.

import streamlit as st
from processing import document_cleaner, keyword_extractor_nltk
from processing.keyword_extractor_nltk import extract_keywords
from processing.matcher_nltk import calculate_matching_scores, get_text_from_docx, get_text_from_pdf
import pandas as pd
import matplotlib.pyplot as plt

def resume_to_job_description_matching_scorer():
    st.subheader("Optimize Your Job Applications")
    resume_text = get_input_text("Resume")
    job_description_text = get_input_text("Job Description")

    # Submit button for matching score calculation
    if st.button('Calculate Matching Score'):
        if resume_text and job_description_text:
            score = calculate_matching_scores(resume_text, job_description_text)
            interpretation = interpret_score(score)
            st.write(f"Matching Score: {score:.2f} - {interpretation}")
            plot_matching_score(score)
        else:
            st.error("Please provide both resume and job description texts.")

def plot_matching_score(score):
    df = pd.DataFrame({'Matching Score': [score]})
    plt.figure(figsize=(8, 4))
    plt.bar(df.index, df['Matching Score'], color='blue')
    plt.xticks(df.index, ['Resume to Job Description'])
    plt.xlabel('Comparison')
    plt.ylabel('Matching Score')
    plt.title('Matching Score between Resume and Job Description')
    st.pyplot(plt)

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

def interpret_score(score):
    if score >= 0.8:
        return 'Excellent Match'
    elif score >= 0.6:
        return 'Good Match'
    elif score >= 0.4:
        return 'Fair Match'
    else:
        return 'Poor Match'

# Main navigation setup
st.sidebar.title("Career Navigation")
menu_option = st.sidebar.selectbox("Menu", ["Services", "User Feedback"])

if menu_option == "Services":
    st.header("Resume to Job Description Matching Scorer")
    resume_to_job_description_matching_scorer()
    st.write("Disclaimer: This is an AI-assisted service and may make mistakes. Users are responsible for verification and validation of the information provided.")

elif menu_option == "User Feedback":
    st.header("User Feedback Form")
    st.write("Your feedback is valuable to us. Please share your thoughts and suggestions.")
    feedback_text = st.text_area("Feedback")
    feedback_rating = st.slider("How would you rate our service?", 1, 5, 3)
    if st.button("Submit Feedback"):
        st.success("Thank you for your feedback! We appreciate your time and input.")

# Define the function used in the Services section
def resume_to_job_description_matching_scorer():
    # Assume some functionality here that processes input and shows outputs
    st.write("")

# Main function to run the Streamlit app
def main():
    if menu_option == "Services":
        st.header("")
        st.write("Use this tool to compare your resume against job descriptions to gauge the match quality.")
        resume_to_job_description_matching_scorer()

# Check if the script is run as the main program and launch Streamlit app
if __name__ == "__main__":
    main()