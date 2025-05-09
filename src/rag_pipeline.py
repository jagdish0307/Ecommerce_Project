import pickle
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from user_history import log_user_interaction

# Load FAISS index, DataFrame, and model from pickle
with open("embeddings/faiss_index.pkl", "rb") as f:
    index, df, model = pickle.load(f)

# Load ID map
with open("embeddings/id_map.pkl", "rb") as f:
    id_map = pickle.load(f)

def build_query_from_attributes(attributes):
    """Combine extracted attributes into a semantic query string."""
    return " ".join(attributes)

def search_products(attributes, user_id=None, original_query=None, top_k=5):
    query_text = build_query_from_attributes(attributes)
    query_vector = model.encode([query_text], convert_to_numpy=True).astype('float32')

    distances, indices = index.search(query_vector, top_k)
    results = []

    for i, idx in enumerate(indices[0]):
        if idx in id_map:
            row_index = id_map[idx]
            product_data = df.iloc[row_index].to_dict()
            product_data["semantic_score"] = float(distances[0][i])
            results.append(product_data)

            # Log user interaction if user_id and original query are provided
            if user_id and original_query:
                log_user_interaction(user_id, original_query, product_data["Product"])

    return results

if __name__ == "__main__":
    sample_attributes = ["lightweight", "student", "SSD", "Ryzen"]
    user_id = "user_123"
    query = "Suggest a laptop which has 16GB RAM and is lightweight."

    matches = search_products(sample_attributes, user_id=user_id, original_query=query)

    for match in matches:
        print(f"\nProduct: {match['Product']}\nSpecs: {match}\n")
