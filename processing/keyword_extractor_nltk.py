import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords, names
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

# Ensure NLTK resources are downloaded
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('names')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('maxent_ne_chunker')
nltk.download('words')

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
# Stop words and common names already defined above

# Additional custom stop words
custom_stop_words = ["noye", "harry", "david", "emmanuel", "daniel", "d", "john", "mary"]
stop_words.extend(custom_stop_words)

# Regular expressions for names (adjust as needed)
name_patterns = [r"\b[A-Z][a-z]+\b", r"\b[A-Z][a-z]+ [A-Z][a-z]+\b"]

# Function to filter text based on stop words and name patterns
def filter_text(text):
    tokens = word_tokenize(text)
    pos_tags = pos_tag(tokens)
    filtered_tokens = [word for word, tag in pos_tags if word.lower() not in stop_words and not any(re.match(pattern, word) for pattern in name_patterns)]
    return " ".join(filtered_tokens)

# Example usage
text = "Dr. David Noye is the CEO of Acme Inc."
filtered_text = filter_text(text)
print(filtered_text)  # Output: "CEO Acme Inc."

# ==================== Document Comparison Functionality ====================
# The compare_documents function remains unchanged as it does not depend on spaCy or NLTK

# ==================== Job Description and Resume Category Mapping Functionality ====================
# The extract_job_desc_categories and extract_resume_categories functions need to be adapted to use NLTK for NER tasks.
# Here's an example modification for extract_resume_categories:

def extract_resume_categories(text):
    tokens = word_tokenize(text)
    pos_tags = pos_tag(tokens)
    ne_chunked = nltk.ne_chunk(pos_tags, binary=False)
    categories = []
    for chunk in ne_chunked:
        if hasattr(chunk, 'label'):
            categories.append(chunk.label())
    return list(set(categories))

# Keyword Extraction Functionality
def extract_keywords(text, top_n=10, stop_words='english', ngram_range=(1, 1)):
    # Initialize NLTK's lemmatizer
    lemmatizer = WordNetLemmatizer()

    # Tokenize and lemmatize the text
    tokens = word_tokenize(text)
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]

    # Use regular expressions to further remove email addresses and other patterns
    clean_text = " ".join(lemmatized_tokens)
    clean_text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', clean_text)  # Remove emails
    clean_text = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '', clean_text)  # Remove IP addresses
    clean_text = re.sub(r'\b\d{5,}\b', '', clean_text)  # Remove long numbers

    # Initialize TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(stop_words=stop_words, ngram_range=ngram_range)
    tfidf_matrix = vectorizer.fit_transform([clean_text])

    # Extract feature names and their corresponding scores
    feature_array = vectorizer.get_feature_names_out()
    tfidf_sorting = tfidf_matrix.toarray().flatten().argsort()[-top_n:]

    # Extract top N keywords based on TF-IDF scores
    top_keywords = [feature_array[i] for i in tfidf_sorting[::-1]]

    return top_keywords

# The categorize_keywords function remains unchanged as it does not depend on spaCy or NLTK
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
