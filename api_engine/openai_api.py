import openai
import os
from dotenv import load_dotenv


# 2 Load the openai environment variables from the .env file: OpenAI Client & API Key
client = openai.Client()
openai.api_key = os.getenv("OPENAI_KEY")


def generate_text(prompt, engine="gpt-3.5-turbo-instruct", max_tokens=150, n=1, stop=None, temperature=0.7, **kwargs):
    """
    Generates text using the OpenAI API's model.
    """
    try:
        response = client.completions.create(
            model=engine,
            prompt=prompt,
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.3,
            **kwargs
        )
        return response.choices[0].text.strip()
    except Exception as e:
        raise Exception(f"Error communicating with OpenAI API: {e}") from e

def search_documents(query, **kwargs):
    """
    Searches documents using the OpenAI API's search function.
    """
    response = openai.Engine("text-davinci-003").search(query, **kwargs)
    return response
