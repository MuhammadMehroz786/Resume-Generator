import textstat
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

# Ensure NLTK resources are downloaded
nltk.download('punkt')

def analyze_sentence_complexity(text):
    # Calculate readability scores using textstat
    gunning_fog_index = textstat.gunning_fog(text)
    flesch_reading_ease = textstat.flesch_reading_ease(text)
    
    # Analyze sentence lengths using NLTK
    sentences = sent_tokenize(text)
    sentence_lengths = [len(word_tokenize(sent)) for sent in sentences]
    
    return gunning_fog_index, flesch_reading_ease, sentence_lengths

def suggest_sentence_improvements(resume_text, job_description_text, resume_keywords, job_desc_keywords):
    sentences_resume = sent_tokenize(resume_text)
    suggestions = []

    # Find keywords in job description not mentioned in the resume
    missing_keywords = [kw for kw in job_desc_keywords if kw not in resume_keywords]
    if missing_keywords:
        suggestions.append(f"Consider adding these skills/qualifications from the job description to your resume: {', '.join(missing_keywords)}")

    # Suggest improvements based on sentence analysis
    for sent in sentences_resume:
        words = word_tokenize(sent)
        if len(words) > 25:  # Threshold for sentence length can be adjusted
            suggestions.append(f"Consider breaking down long sentences for clarity: '{sent[:50]}...'")

        # Suggest using active voice for more direct sentences
        # Note: NLTK does not provide dependency parsing like spaCy, so this might be less straightforward to implement.

    # Suggest simplifying technical jargon or complex terms
    for word in word_tokenize(resume_text):
        if word in missing_keywords:
            suggestions.append(f"Clarify or define industry-specific terms or skills: '{word}'")

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
