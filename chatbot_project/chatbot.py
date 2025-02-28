import json
import numpy as np
import google.generativeai as genai
from sentence_transformers import SentenceTransformer

# Load Gemini API key
GEMINI_API_KEY = "AIzaSyAXHYO4AWe3KKKg9mqjebImGyExD7hxjO8"
genai.configure(api_key=GEMINI_API_KEY)

# Load embeddings and documentation
with open("data/embeddings.json", "r") as f:
    embeddings_data = json.load(f)

with open("data/documentation.json", "r") as f:
    documentation = json.load(f)

# Convert stored embeddings to NumPy arrays
for key in embeddings_data:
    embeddings_data[key] = np.array(embeddings_data[key])

# Load sentence transformer model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Function to find the most relevant docs
def retrieve_top_docs(query, top_n=2):
    query_embedding = model.encode(query)
    
    similarities = {
        doc_name: np.dot(query_embedding, doc_embedding) / 
        (np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding))
        for doc_name, doc_embedding in embeddings_data.items()
    }
    
    top_docs = sorted(similarities, key=similarities.get, reverse=True)[:top_n]
    return top_docs

# Function to generate an answer using Gemini AI
def generate_answer(query):
    top_docs = retrieve_top_docs(query)
    relevant_texts = " ".join([documentation[doc] for doc in top_docs if doc in documentation])

    # Use a Gemini model
    model = genai.GenerativeModel("gemini-2.0-pro-exp")  # Change model if needed

    response = model.generate_content(f"Context: {relevant_texts} \n\nQuestion: {query}")

    return response.text if response else "Sorry, I couldn't generate an answer."

# Interactive chat loop
while True:
    query = input("Ask something: ")
    if query.lower() == "exit":
        break
    
    answer = generate_answer(query)
    print("\nAI Answer:", answer)
