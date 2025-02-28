from sentence_transformers import SentenceTransformer
import json
import numpy as np

# Load the pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load the scraped documentation
with open('data/documentation.json', 'r', encoding='utf-8') as json_file:
    docs = json.load(json_file)

embeddings = {}

# Generate embeddings for each platform
for platform, content in docs.items():
    print(f"Generating embeddings for {platform}...")
    embedding = model.encode(content)  # Convert text into embeddings
    embeddings[platform] = embedding.tolist()  # Convert NumPy array to list for saving

# Save embeddings to a file
with open('data/embeddings.json', 'w', encoding='utf-8') as json_file:
    json.dump(embeddings, json_file, indent=4)

print("Embeddings generated and saved in data/embeddings.json")
