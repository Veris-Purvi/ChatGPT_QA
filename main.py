import openai
import pandas as pd
from openai.embeddings_utils import cosine_similarity
from openai.embeddings_utils import get_embedding
import json
from flask import Flask, request
from pyngrok import ngrok, conf, installer
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('.env')

# Set the OpenAI API key from the environment variable
openai.api_key = os.environ['API_KEY']

# Create a Flask application
app = Flask(__name__)

@app.route('/')
def welcome():
    return {"msg": "Welcome", "status": "success"}

@app.route('/predict')
def predict():
    # Read the trial.csv file containing the question embeddings
    emb = pd.read_csv('trial.csv')
    
    # Remove duplicate questions from the DataFrame
    emb = emb.drop_duplicates(subset="Questions")
    
    # Convert the 'embedding' column to a list of lists of floats
    emb['embedding'] = emb['embedding'].apply(lambda x: '[]' if x is None or not isinstance(x, str) else x)
    emb['embedding'] = emb['embedding'].apply(eval)
    emb['embedding'] = emb['embedding'].apply(lambda x: [float(i) for i in x])
    
    # Get the question from the request arguments
    question = request.args.get('question')
    
    # Get the embedding vector for the question
    question_vector = get_embedding(question, engine='text-embedding-ada-002')
    
    # Calculate the cosine similarity between the question and the embeddings
    emb["similarities"] = emb['embedding'].apply(lambda x: cosine_similarity(x, question_vector) if len(x) > 0 else 0)
    
    # Sort the DataFrame by similarities in descending order and select the top 4 most similar questions
    emb = emb.sort_values("similarities", ascending=False).head(4)
    
    # Extract the context from the selected questions
    context = []
    for i, row in emb.iterrows():
        context.append(row['Combined'])
    text = "\n".join(context)
    context = text
    
    # Create the prompt for OpenAI Completion API
    prompt = f"""Answer the following question using only the context below.

    Context:
    {context}

    Q: {question}
    A:"""

    try:
        # Generate the answer using OpenAI Completion API
        ans = openai.Completion.create(
            prompt=prompt,
            temperature=1,
            max_tokens=200,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            model="text-davinci-003",
        )["choices"][0]["text"].strip(" \n")

        return ans
    except Exception as e:
        return {"msg": e, "status": "error"}

if __name__ == '__main__':
    app.run(port=3000)
