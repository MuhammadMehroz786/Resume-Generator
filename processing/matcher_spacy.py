import pandas as pd
import docx
from docx import Document  # Import for docx parsing (if still needed)
import fitz  # PyMuPDF

#############
# MODEL LOADING
#############

import spacy  # Library for advanced text analysis and NLP
from spacy.cli import download

# Global variable to hold the loaded spaCy model
nlp = None

def get_spacy_model(model_name="en_core_web_sm"):
    """Lazily loads or downloads the specified spaCy model."""
    global nlp
    if nlp is None:
        try:
            nlp = spacy.load(model_name)
        except IOError:
            print(f"Model {model_name} not found, downloading...")
            download(model_name)
            nlp = spacy.load(model_name)
    return nlp

# Define keyword weights (optional)
"""
Assigns weights to keywords to adjust their importance in matching calculations.
Higher weights indicate greater relevance.
"""
keyword_weights = {
    "python": 2.0,  # Prioritize Python skills
    "data analysis": 1.5,  # Moderate emphasis on data analysis
    "machine learning": 2.5,  # Strong emphasis on machine learning
    "java": 1.0,  # Neutral weight for Java
    "sql": 1.2,  # Slightly higher weight for SQL
    "data visualization": 1.4,  # Moderate weight for data visualization
    # Add more keywords and weights as needed
}

# Function to read text from DOCX
def get_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    return "\n".join([para.text for para in doc.paragraphs])

# Function to read text from PDF
def get_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Function to extract keywords using spaCy
def extract_keywords(text):
    doc = nlp(text)
    keywords = [token.text for token in doc if not token.is_stop and not token.is_punct and token.pos_ in ["NOUN", "PROPN", "VERB"]]
    return [(kw, keyword_weights.get(kw, 1.0)) for kw in keywords]

# Function to calculate cosine similarity: Often used in natural language processing and information retrieval tasks to measure the similarity between text documents or other data represented as vectors.

def calculate_cosine_similarity(vec1, vec2):
    """
    Calculate cosine similarity between two vectors represented as dictionaries.

    Args:
        vec1 (dict): The first vector represented as a dictionary.
        vec2 (dict): The second vector represented as a dictionary.

    Returns:
        float: The cosine similarity between the two vectors. A value between -1.0 and 1.0.
    """
    # Find the intersection of keys between vec1 and vec2
    intersection = set(vec1.keys()) & set(vec2.keys())

    # Calculate the numerator of the cosine similarity formula
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    # Calculate the sum of squares of vector elements for vec1
    sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])

    # Calculate the sum of squares of vector elements for vec2
    sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])

    # Calculate the denominator of the cosine similarity formula
    denominator = (sum1 ** 0.5) * (sum2 ** 0.5)

    # Check if the denominator is zero (to avoid division by zero)
    if not denominator:
        return 0.0
    else:
        # Calculate and return the cosine similarity
        return float(numerator) / denominator

# Main function to calculate matching scores
def calculate_matching_scores(resume_text, job_description_text):
    resume_keywords = extract_keywords(resume_text)
    job_desc_keywords = extract_keywords(job_description_text)
    
    resume_vector = pd.Series({k: v for k, v in resume_keywords})
    job_desc_vector = pd.Series({k: v for k, v in job_desc_keywords})
    
    return calculate_cosine_similarity(resume_vector, job_desc_vector)

    # Compare resume skills with job description skills based on categories
    matching_scores = {}
    for resume_category, resume_skills in resume_categories.items():
        if resume_category in job_desc_categories:
            job_desc_skills = job_desc_categories[resume_category]
            score = calculate_cosine_similarity(resume_skills, job_desc_skills)
            matching_scores[resume_category] = score

    # Return dictionary with category-wise matching scores
    return matching_scores

# Passing the variables as arguments:
# Example usage
if __name__ == "__main__":
    resume_text = "Your resume text or use get_text_from_docx/pdf to load"
    job_description_text = "Your job description text or use get_text_from_docx/pdf to load"
    scores = calculate_matching_scores(resume_text, job_description_text)  # Pass only the required arguments