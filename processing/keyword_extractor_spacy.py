# Keyword_Extactor file: (a) extracts keywords, (b)facilitates further analysis and matching, and (c) promotes flexibility and customization
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords, names
from nltk.stem import WordNetLemmatizer

# Load a spaCy model for English
import spacy  # Library for advanced text analysis and NLP
from spacy.cli import download

# Initialize a global variable for the spaCy NLP model
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

# Ensure nlkt resources are downloaded (e.g., WordNet)
from nltk.corpus import wordnet as wn   # It's used in the aggregate_terms function to. the wn import remains crucial for these WordNet-related operations within the script

# Ensure NLTK resources are downloaded (only once)
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('names')

# Stop words (combined with common names) to enhance filtering
stop_words = stopwords.words('english')
common_names = set(names.words())
stop_words.extend(common_names)

# ==================== Document Comparison Functionality ====================
# Get English stopwords
stop_words = stopwords.words('english')

# Define additional custom stopwords
custom_stop_words = ["noye", "dr", "david", "orcid", "i", "d", "he", "ceo"]
stop_words.extend(custom_stop_words)

# ==================== Document Comparison Functionality ====================
# import nltk
from nltk.corpus import stopwords, names

# Download resources if needed
nltk.download('names')

# Built-in stop words
stop_words = stopwords.words('english')

# Common names
common_names = set(names.words())
stop_words.extend(common_names)

# Download the corpus (if needed):
nltk.corpus.names

# Access names
common_names = set(nltk.corpus.names.words())

# Additional custom stop words
custom_stop_words = ["noye", "harry", "david", "emmanuel", "daniel", "d", "john", "mary"]
stop_words.extend(custom_stop_words)

# Regular expressions for names (adjust as needed)
name_patterns = [r"\b[A-Z][a-z]+\b", r"\b[A-Z][a-z]+ [A-Z][a-z]+\b"]

# Function to filter text based on stop words and name patterns
def filter_text(text):
    filtered_words = []
    for word in text.split():
        if word.lower() not in stop_words and not any(re.match(pattern, word) for pattern in name_patterns):
            filtered_words.append(word)
    return " ".join(filtered_words)

# Example usage
text = "Dr. David Noye is the CEO of Acme Inc."
filtered_text = filter_text(text)
print(filtered_text)  # Output: "ceo acme inc"

# ==================== Document Comparison Functionality ====================
def compare_documents(doc1, doc2):
    """
    Compares two documents and calculates their similarity using the cosine similarity metric.

    Args:
        doc1 (str): Text of the first document.
        doc2 (str): Text of the second document.

    Returns:
        float: Cosine similarity score between the two documents.
    """
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([doc1, doc2])
    similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return similarity_matrix[0][0]

# ==================== Job Description Category Mapping Functionality ====================
def extract_job_desc_categories(job_desc_text):
    """
    Extracts categories from job descriptions using a combination of rule-based logic and machine learning (ML).

    Args:
        job_desc_text (str): The text of the job description to process.

    Returns:
        dict: A dictionary containing the extracted categories and their corresponding text snippets.
    """

    categories = {}

    # ==================== Rule-Based Logic ====================

    # Define rules for each category using keywords, patterns, or regular expressions:

    # Job Title
    title_match = re.search(r"^Job Title:\s*(.*)", job_desc_text, flags=re.IGNORECASE | re.MULTILINE)
    if title_match:
        categories["Job Title"] = title_match.group(1).strip()

    # ... Add rules for other categories (e.g., Department, Reports To, etc.) ...

    # ==================== Machine Learning (Placeholder for Future Integration) ====================

    # # Load pre-trained ML model or train a custom model (commented for now)
    # # ml_model = ...

    # # Use model to predict additional categories or refine rule-based results (commented for now)
    # # ml_predictions = ml_model.predict(job_desc_text)
    # # ... integrate ML predictions with rule-based results ...

    return categories

# ==================== Resume Category Mapping Functionality ====================

def extract_resume_categories(text):
    """
    Extracts categories from the resume text using a combination of NER and rule-based approach.

    Args:
        text (str): Resume text to extract categories from.

    Returns:
        list: List of extracted categories.
    """

    categories = []

    # 1. Named Entity Recognition (NER)
    doc = nlp(text)
    for entity in doc.ents:
        if entity.label_ in ["GPE", "LOC"]:  # Filter out locations and organizations
            continue
        categories.append(entity.label_)

    # 2. Rule-based approach
    for word in text.lower().split():
        if word in ["skills", "experience"]:
            categories.append("Skills")
        if word in ["education", "degree"]:
            categories.append("Education")
        # ... add more rules for different sections and categories

    # 3. Remove duplicates and ensure unique categories
    return list(set(categories))

# # Define the find_matching_categories function here:
def find_matching_categories(keyword, skills_taxonomy):
    """Finds categories in the skills taxonomy that match the given keyword."""

    matching_categories = []

    # Example implementation using exact matching:
    for category, skills in skills_taxonomy.items():
        if keyword in skills:
            matching_categories.append(category)

    # Consider using fuzzy matching techniques for broader matches:
    # for category, skills in skills_taxonomy.items():
    #     for skill in skills:
    #         similarity = fuzzywuzzy.fuzz.ratio(keyword, skill)  # Example using fuzzywuzzy
    #         if similarity >= 80:  # Adjust threshold as needed
    #             matching_categories.append(category)
    #             break  # Move to the next category if a match is found

    return matching_categories


# ==================== Keyword Extraction Functionality ====================
def extract_keywords(text, top_n=10, stop_words='english', ngram_range=(1, 1)):
    """
    Extracts top N keywords from the given text using TF-IDF, excluding personal information.

    Args:
        text (str): The input text to extract keywords from.
        top_n (int): The number of top keywords to return.

    Returns:
        list: A list of top N keywords extracted from the text.
    """
    # Use spaCy for named entity recognition to filter out personal names
    doc = nlp(text)
    entities_to_exclude = {'PERSON', 'GPE', 'ORG', 'DATE'}

    filtered_tokens = [token.lemma_ for token in doc if token.ent_type_ not in entities_to_exclude]

    # Use regular expressions to further remove email addresses and other patterns
    clean_text = " ".join(filtered_tokens)
    clean_text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', clean_text)  # Remove emails
    clean_text = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '', clean_text)  # Remove IP addresses
    clean_text = re.sub(r'\b\d{5,}\b', '', clean_text)  # Remove long numbers that could be zip codes or phone numbers

    # Initialize TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(stop_words=stop_words, ngram_range=ngram_range)
    tfidf_matrix = vectorizer.fit_transform([clean_text])

    # Extract feature names and their corresponding scores
    feature_array = vectorizer.get_feature_names_out()
    tfidf_sorting = tfidf_matrix.toarray().flatten().argsort()[-top_n:]

    # Extract top N keywords based on TF-IDF scores
    top_keywords = [feature_array[i] for i in tfidf_sorting[::-1]]

    return top_keywords


# Categorize keywords (if skills taxonomy is loaded successfully)
def categorize_keywords(top_keywords, skills_taxonomy):
    """Categorizes keywords based on a provided skills taxonomy.

    Args:
        top_keywords (list): A list of the most relevant keywords extracted from a resume or job description.
        skills_taxonomy (dict): A dictionary representing a skills taxonomy, where keys are skill categories and values are lists of related keywords.

    Returns:
        dict: A dictionary where keys are skill categories and values are lists of keywords matching those categories.
             If skills_taxonomy is not provided or errors occur, returns an empty dictionary.
    """

    # Initialize empty dictionary to store categorized keywords
    categorized_keywords = {}

    # Categorize keywords only if a skills taxonomy is provided
    if skills_taxonomy:
        # Iterate through each top keyword
        for keyword in top_keywords:
            # Find matching categories for the current keyword
            matching_categories = find_matching_categories(keyword, skills_taxonomy)

            # Add the keyword to its matching categories
            for category in matching_categories:
                if category not in categorized_keywords:
                    # Create a new list for the category if it doesn't exist
                    categorized_keywords[category] = []
                categorized_keywords[category].append(keyword)

    return categorized_keywords  # Return categorized keywords (or an empty dictionary if errors occurred)

def filter_text(text):
    """Filters out names from the given text using regular expressions."""

    # Example regular expression to remove names:
    filtered_text = re.sub(r"\b(?:[A-Z][a-z]+\s+){1,2}\w+\b", "", text)

    return filtered_text  # Return the filtered text

    
def aggregate_terms(terms, scores):
    """
    Aggregates terms into clusters based on their semantic similarity using WordNet.

    Args:
    terms (list): List of terms to be aggregated.
    scores (list): List of scores corresponding to each term.

    Returns:
    list: A list of clusters with each cluster being a list of indices of related terms.
    """
    lemmatizer = WordNetLemmatizer()
    clusters = []

    for i, term1 in enumerate(terms):
        term1_lemma = lemmatizer.lemmatize(term1)
        cluster = [i]  # Start a cluster with the current term index

        for j, term2 in enumerate(terms):
            if i == j:
                continue  # Skip the same term comparison
            term2_lemma = lemmatizer.lemmatize(term2)
            # Check if terms have synsets in WordNet
            if wn.synsets(term1_lemma) and wn.synsets(term2_lemma):
                # Compare the first synset of each term for similarity
                similarity = wn.synsets(term1_lemma)[0].path_similarity(wn.synsets(term2_lemma)[0])
                if similarity and similarity >= 0.7:  # Consider a threshold for similarity
                    cluster.append(j)  # Add index of similar term to the cluster

        clusters.append(cluster)

    return clusters

# Example usage:
# text = "Your text here."
# keywords = extract_keywords(text)
# print("Extracted Keywords:", keywords)
