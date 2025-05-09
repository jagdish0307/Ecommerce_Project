from user_history import log_user_interaction, get_user_history
from rag_pipeline import search_products
from llm_query_handler import understand_query
from llm_recommendation import generate_recommendation

def personalized_laptop_search(user_id, user_query, top_k=5):
    # Step 1: Understand the current user query
    query_json = understand_query(user_query)
    print(f"[DEBUG] Parsed query: {query_json}")

    # Step 2: Build attribute list from parsed query
    import json
    parsed = json.loads(query_json)
    attributes = []
    imp = parsed.get("important_attributes", {})
    if imp.get("lightweight"): attributes.append("lightweight")
    if imp.get("price_under"): attributes.append(f"under {imp['price_under']} euros")
    if imp.get("price_above"): attributes.append(f"above {imp['price_above']} euros")
    if imp.get("brand"): attributes.append(imp["brand"])
    if imp.get("model"): attributes.append(imp["model"])
    if imp.get("use_case"): attributes.append(imp["use_case"])

    # Step 3: Personalize using user history
    history = get_user_history(user_id)
    if history:
        history_keywords = " ".join([h[2] for h in history])  # concatenate previous product names
        attributes.append(history_keywords)
        print(f"[DEBUG] Personalizing with history: {history_keywords}")

    # Step 4: Search via semantic RAG pipeline
    results = search_products(attributes, top_k=top_k)

    # Step 5: Generate natural language recommendation
    recommended = generate_recommendation(user_query, results)

    # Step 6: Log this interaction
    if results:
        log_user_interaction(user_id, user_query, results[0].get("Product"))

    return recommended

# For testing
if __name__ == "__main__":
    user_id = "user123"
    query = "Suggest something good for college work"
    response = personalized_laptop_search(user_id, query)
    print(f"\n[RECOMMENDATION]\n{response}")
