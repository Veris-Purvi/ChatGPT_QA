import pandas as pd
import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('.env')

# Set the OpenAI API key from the environment variable
openai.api_key = os.environ['API_KEY']

# Function to retrieve text embeddings
def get_embedding(text, model):
    embedding = openai.Embedding.create(
        input=text,
        model=model
    )["data"][0]["embedding"]
    return embedding

# Read the questions.csv file using pandas
# Ensure that the file contains a column named 'Combined' where the data from both the question and answer cells are merged
# If the 'Combined' column is not present, you can create it by merging the 'Question' and 'Answer' columns using the CONCATENATE function, e.g., =CONCATENATE(A1, B1)
df = pd.read_csv('questions.csv')

ref = df
embedding_list = []
for row in ref['Combined']:
    try:
        # Get the embedding for the current row using the specified model
        embedding = get_embedding(row, model='text-embedding-ada-002')
        embedding_list.append(embedding)
    except Exception as e:
        # Handle exceptions if embedding retrieval fails
        print(e)
        print("hi")
        embedding_list.append(None)

# Add the 'embedding' column to the dataframe
ref['embedding'] = embedding_list

# Save the dataframe to trial.csv
ref.to_csv('trial.csv')
