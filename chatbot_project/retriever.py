import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load the embeddings
with open("data/embeddings.json", "r") as f:
    embeddings_data = json.load(f)

documents = list(embeddings_data.keys())  # Document names
embeddings = np.array(list(embeddings_data.values()), dtype="float32")  # Convert embeddings to NumPy array

# Initialize FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])  # L2 distance for similarity search
index.add(embeddings)  # Add embeddings to index

# Load model for encoding queries
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def retrieve_top_docs(query, top_k=2):
    """Retrieve top matching documentation sections based on query"""
    query_embedding = model.encode([query])[0]  # Convert query to embedding
    query_embedding = np.array([query_embedding], dtype="float32")  # Ensure correct format

    _, indices = index.search(query_embedding, top_k)  # Search for similar vectors
    results = [documents[i] for i in indices[0]]  # Get document names

    return results


if __name__ == "__main__":
    while True:
        user_query = input("\nAsk something: ")
        if user_query.lower() in ["exit", "quit"]:
            break

        results = retrieve_top_docs(user_query)
        print(f"\nTop matching docs: {results}")
