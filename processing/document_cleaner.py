# Import necessary libraries (e.g., os, re, nltk).
import os, re, nltk 

nltk.download('punkt')  # Download the Punkt sentence tokenizer if needed

# Define a function to load text from a file:
def load_text_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            return text
    except FileNotFoundError:
        print("Error: File not found at the specified path. Please check the file path or provide a valid resume file.")
        return None  # Return None or handle the missing file appropriately


# Define a function to clean text:
# Function to clean text
def clean_text(text):
    if text:  # Only process if text is not None
        # Remove punctuation
        text = re.sub(r'[^\w\s]', '', text)

        # Convert to lowercase
        text = text.lower()

        # Tokenize into words
        words = nltk.word_tokenize(text)

        # Optionally apply stemming or lemmatization (uncomment and implement as needed)
        # ...

        return ' '.join(words)  # Rejoin words into a string
    else:
        return None  # Or handle the case of missing text differently

# Example usage (commented out for clarity)
# file_path = 'data/resumes/sample_resume.txt'  # Replace with a sample resume file
# text = load_text_from_file(file_path)
# cleaned_text = clean_text(text)
# print(cleaned_text)