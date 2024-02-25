import os
from openai import OpenAI

def get_vector_embedding(message_string):

    api_key = os.getenv('OPENAI_API_KEY')

    if api_key is None:
        raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

    client = OpenAI(api_key= api_key)

    model="text-embedding-3-small"

    message_string = message_string.replace("\n", " ")
    return client.embeddings.create(input = [message_string], model=model).data[0].embedding