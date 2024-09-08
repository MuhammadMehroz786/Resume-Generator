import textstat

# Load a language model for text analysis
import spacy
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


def analyze_sentence_complexity(text):
    doc = nlp(text)
    # Calculate readability scores
    gunning_fog_index = textstat.gunning_fog(text)
    flesch_reading_ease = textstat.flesch_reading_ease(text)
    # Analyze sentence lengths and patterns
    sentence_lengths = [len(sent) for sent in doc.sents]
    return gunning_fog_index, flesch_reading_ease, sentence_lengths

def suggest_sentence_improvements(resume_text, job_description_text, resume_keywords, job_desc_keywords):
    doc_resume = nlp(resume_text)
    suggestions = []

    # Find keywords in job description not mentioned in the resume
    missing_keywords = [kw for kw in job_desc_keywords if kw not in resume_keywords]
    if missing_keywords:
        suggestions.append(f"Consider adding these skills/qualifications from the job description to your resume: {', '.join(missing_keywords)}")

    # Suggest improvements based on sentence analysis
    for sent in doc_resume.sents:
        if len(sent.text.split()) > 25:  # Threshold for sentence length can be adjusted
            suggestions.append(f"Consider breaking down long sentences for clarity: '{sent.text[:50]}...'")

        # Suggest using active voice for more direct sentences
        for token in sent:
            if token.dep_ == "auxpass":
                suggestions.append(f"Consider using active voice for more impact: '{sent.text[:50]}...'")

    # Suggest simplifying technical jargon or complex terms
    for token in doc_resume:
        if token.tag_ in ["JJ", "NNP"] and token.text in missing_keywords:
            suggestions.append(f"Clarify or define industry-specific terms or skills: '{token.text}'")

    # Eliminate redundancies and improve conciseness
    redundant_phrases = ["in order to", "due to the fact that", "at this point in time"]
    for phrase in redundant_phrases:
        if phrase in resume_text:
            suggestions.append(f"Eliminate redundancies for conciseness: Replace '{phrase}' with a simpler alternative.")

    return suggestions

# Test the function
# text = "This is a sample sentence for analysis. Despite the fact that it's only an example, it serves to demonstrate the function."
# complexity_scores = analyze_sentence_complexity(text)
# print("Complexity Scores:", complexity_scores)
# suggestions = suggest_sentence_improvements(text)
# print("Improvement Suggestions:", suggestions)
