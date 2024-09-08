import pandas as pd
import docx
import fitz  # PyMuPDF
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

# Ensure NLTK resources are downloaded
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Define keyword weights (optional)
keyword_weights = {
    "python": 2.0,
    "data analysis": 1.5,
    "machine learning": 2.5,
    "java": 1.0,
    "sql": 1.2,
    "data visualization": 1.4,
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

# Function to extract keywords using NLTK
def extract_keywords(text):
    stop_words_set = set(stopwords.words('english'))
    tokens = word_tokenize(text)
    pos_tags = pos_tag(tokens)
    keywords = [token for token, tag in pos_tags if token.lower() not in stop_words_set and tag in ["NN", "NNS", "NNP", "NNPS", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]]
    return [(kw, keyword_weights.get(kw.lower(), 1.0)) for kw in keywords]

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

# Example usage
if __name__ == "__main__":
    resume_text = "Your resume text or use get_text_from_docx/pdf to load"
    job_description_text = "Your job description text or use get_text_from_docx/pdf to load"
    scores = calculate_matching_scores(resume_text, job_description_text)
