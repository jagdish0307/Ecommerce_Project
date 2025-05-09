import pickle
import json
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from llm_query_handler import understand_query

# Load FAISS index, DataFrame, and model
with open("embeddings/faiss_index.pkl", "rb") as f:
    index, df, model = pickle.load(f)

def clean_llm_response(response_text):
    if response_text.startswith("```"):
        response_text = response_text.strip().strip("```").replace("json", "").strip()
    return response_text
def apply_filters(query_analysis, results_df):
    filters = query_analysis.get("important_attributes", {})

    # Price filters
    if isinstance(filters.get("price_under"), (int, float)):
        results_df = results_df[results_df["Price_euros"] <= filters["price_under"]]
    if isinstance(filters.get("price_above"), (int, float)):
        results_df = results_df[results_df["Price_euros"] >= filters["price_above"]]

    # Lightweight filter
    if filters.get("lightweight") is True:
        results_df = results_df[results_df["Weight"] < 2.0]

    # Brand filter
    brand = filters.get("brand")
    if isinstance(brand, str) and brand.strip():
        results_df = results_df[
            results_df["Company"].fillna("").str.lower().str.contains(brand.strip().lower(), na=False)
        ]

    # Model filter
    model = filters.get("model")
    if isinstance(model, str) and model.strip():
        results_df = results_df[
            results_df["Product"].fillna("").str.lower().str.contains(model.strip().lower(), na=False)
        ]

    # Use-case filter
    use_case_raw = filters.get("use_case")
    use_case = use_case_raw.lower() if isinstance(use_case_raw, str) else ""

    if use_case:
        use_case_synonyms = {
            "gaming": ["gaming", "gamer"],
            "student": ["student", "college", "school"],
            "office": ["office", "business", "work"],
            "video editing": ["video editing", "content creation", "editing"]
        }

        # Normalize use case
        for key, synonyms in use_case_synonyms.items():
            if any(s in use_case for s in synonyms):
                use_case = key
                break

        if use_case == "gaming":
            results_df = results_df[
                (results_df["Ram"] >= 8) &
                (results_df["GPU_model"].fillna("").str.contains("GTX|RTX", case=False, na=False))
            ]
        elif use_case == "student":
            results_df = results_df[
                (results_df["Weight"] < 2.0) &
                (results_df["Price_euros"] < 1000)
            ]
        elif use_case == "office":
            results_df = results_df[results_df["Weight"] < 2.0]
        elif use_case == "video editing":
            results_df = results_df[
                (results_df["Ram"] >= 16) &
                (results_df["GPU_model"].fillna("").str.contains("GTX|RTX|Quadro", case=False, na=False))
            ]

    return results_df



def search_laptops(user_query, top_k=5):
    print(f"[INFO] User query: {user_query}")

    llm_response = understand_query(user_query)
    print(f"[DEBUG] LLM response: {llm_response}")

    try:
        query_data = json.loads(clean_llm_response(llm_response))
    except Exception as e:
        print(f"[WARN] LLM parsing failed, fallback to semantic only. Reason: {e}")
        query_data = {"important_attributes": {}}

    # Semantic search
    embedding = model.encode([user_query], convert_to_numpy=True).astype('float32')
    _, indices = index.search(embedding, top_k)

    result_df = df.iloc[indices[0]].copy()

    # Apply filters
    filtered_df = apply_filters(query_data, result_df)

    if filtered_df.empty:
        return "Sorry, no laptops match your criteria."

    filtered_df = filtered_df.sort_values(by="Price_euros")

    # Format response
    response = "Top Results:\n"
    for _, row in filtered_df.iterrows():
        response += f"\n{row['Product']} by {row['Company']}\n"
        response += f"  - RAM: {row['Ram']} GB\n"
        response += f"  - CPU: {row['CPU_model']}\n"
        response += f"  - GPU: {row['GPU_model']}\n"
        response += f"  - Price: €{row['Price_euros']}\n"
        response += f"  - Weight: {row['Weight']} kg\n"
        response += f"  - Storage: {row['PrimaryStorage']} GB\n"

    return response

if __name__ == "__main__":
    queries = [
        "Suggest a good gaming laptop which has 16GB RAM and is lightweight.",
        "Find laptops for students",
        "Best laptop under 800 euros for school and college",
        "I need a lightweight Dell laptop which weight under 1 kg",
        "High performance laptops for video editing which has above 32 GB RAM",
    ]

    for q in queries:
        print("="*80)
        print(search_laptops(q))
