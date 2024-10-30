import os
import openai

openai.api_key = os.getenv("OPENIA_API_KEY")

def generate_embeddings(text):
    response = openai.embeddings.create(
        input=text,
        model="text-embedding-ada-002" 
    )
    return response.data[0].embedding
