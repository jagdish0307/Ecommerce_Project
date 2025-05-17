
import pandas as pd
import numpy as np
# Assuming these imports exist and work in your project
from llm_query_handler import understand_query  
from vector_store import get_faiss_index, get_embeddings, get_id_map, fetch_laptop_data


def filter_laptops(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    filtered_df = df.copy()

    if filters.get("brand"):
        filtered_df = filtered_df[filtered_df["Company"].str.lower() == filters["brand"].lower()]

    if filters.get("model"):
        filtered_df = filtered_df[filtered_df["Product"].str.lower().str.contains(filters["model"].lower())]

    use_case = filters.get("use_case")
    if use_case:
        if use_case.lower() == "gaming":
            filtered_df = filtered_df[
                (filtered_df["GPU_company"].notnull()) &
                (filtered_df["Ram"] >= 16)
            ]
        elif use_case.lower() == "student":
            filtered_df = filtered_df[
                (filtered_df["Weight"] <= 2) &
                (filtered_df["Price_euros"] <= 800)
            ]
        elif use_case.lower() == "office":
            filtered_df = filtered_df[
                (filtered_df["Ram"] >= 8) &
                (filtered_df["Weight"] <= 2.5)
            ]
        elif use_case.lower() == "remote work":
            filtered_df = filtered_df[
                (filtered_df["Weight"] <= 1.5)
            ]

    if filters.get("price_under") is not None:
        filtered_df = filtered_df[filtered_df["Price_euros"] <= filters["price_under"]]
    if filters.get("price_above") is not None:
        filtered_df = filtered_df[filtered_df["Price_euros"] >= filters["price_above"]]

    if filters.get("ram_under") is not None:
        filtered_df = filtered_df[filtered_df["Ram"] <= filters["ram_under"]]
    if filters.get("ram_above") is not None:
        filtered_df = filtered_df[filtered_df["Ram"] >= filters["ram_above"]]

    if filters.get("storage_under") is not None:
        filtered_df = filtered_df[filtered_df["PrimaryStorage"] <= filters["storage_under"]]
    if filters.get("storage_above") is not None:
        filtered_df = filtered_df[filtered_df["PrimaryStorage"] >= filters["storage_above"]]

    if filters.get("weight_under") is not None:
        filtered_df = filtered_df[filtered_df["Weight"] <= filters["weight_under"]]
    if filters.get("weight_above") is not None:
        filtered_df = filtered_df[filtered_df["Weight"] >= filters["weight_above"]]

    return filtered_df.reset_index(drop=True)


def suggest_relaxations(filters, filtered_df):
    suggestions = []

    if filtered_df.empty:
        if filters.get("brand"):
            suggestions.append(f"Try removing or changing the brand filter (currently '{filters['brand']}').")
        if filters.get("ram_above"):
            suggestions.append(f"Try lowering the RAM requirement (currently > {filters['ram_above']} GB).")
        if filters.get("price_under"):
            suggestions.append(f"Try increasing the price limit (currently < {filters['price_under']} euros).")
        if filters.get("weight_under"):
            suggestions.append(f"Try increasing the weight tolerance (currently < {filters['weight_under']} kg).")
        if filters.get("storage_above"):
            suggestions.append(f"Try lowering the storage requirement (currently > {filters['storage_above']} GB).")

    return suggestions

def search_laptops(df, semantic_results, filters):
    # Step 1: Apply semantic filter
    if semantic_results:
        df = df[df["Product"].isin(semantic_results)]

    # Step 2: Apply structured filters
    if filters.get("brand"):
        df = df[df["Company"].str.lower() == filters["brand"].lower()]
    if filters.get("model"):
        df = df[df["Product"].str.lower().str.contains(filters["model"].lower())]
    if filters.get("use_case"):
        use_case = filters["use_case"].lower()
        if use_case == "gaming":
            df = df[(df["GPU_company"].notnull()) & (df["Ram"] >= 16)]
        elif use_case == "student":
            df = df[(df["Weight"] <= 2) & (df["Price_euros"] <= 800)]
        elif use_case == "office":
            df = df[(df["Ram"] >= 8) & (df["Weight"] <= 2.5)]
        elif use_case == "remote work":
            df = df[df["Weight"] <= 1.5]

    if filters.get("price_under") is not None:
        df = df[df["Price_euros"] <= filters["price_under"]]
    if filters.get("price_above") is not None:
        df = df[df["Price_euros"] >= filters["price_above"]]
    if filters.get("ram_under") is not None:
        df = df[df["Ram"] <= filters["ram_under"]]
    if filters.get("ram_above") is not None:
        df = df[df["Ram"] >= filters["ram_above"]]
    if filters.get("storage_under") is not None:
        df = df[df["PrimaryStorage"] <= filters["storage_under"]]
    if filters.get("storage_above") is not None:
        df = df[df["PrimaryStorage"] >= filters["storage_above"]]
    if filters.get("weight_under") is not None:
        df = df[df["Weight"] <= filters["weight_under"]]
    if filters.get("weight_above") is not None:
        df = df[df["Weight"] >= filters["weight_above"]]

    # Step 3: Check if results exist
    if df.empty:
        suggestions = suggest_relaxations(filters, df)
        return {
            "results": [],
            "message": "No matching laptops found based on your criteria.",
            "suggestions": suggestions
        }

    # Step 4: Prepare structured results with necessary fields
    results = df[["Company", "Product", "Price_euros", "Ram", "PrimaryStorage", "Weight"]].to_dict(orient="records")
    return {
        "results": results,
        "message": f"{len(results)} matching laptops found.",
        "suggestions": []
    }

def format_laptop_results(results):
    formatted = []
    for i, item in enumerate(results[:5], 1):  # Limit to top 5 results
        formatted.append(
            f"{i}. {item['Company']} {item['Product']}\n"
            f"   - RAM: {item['Ram']} GB\n"
            f"   - Storage: {item['PrimaryStorage']} GB\n"
            f"   - Weight: {item['Weight']} kg\n"
            f"   - Price: €{item['Price_euros']}\n"
        )
    return "\n".join(formatted)


if __name__ == "__main__":
    df_laptops = fetch_laptop_data()
    user_query = "give me best laptops for remote work which has above 16GB RAM"

    filters = understand_query(user_query)
    semantic_results = []  # Normally from FAISS

    results_dict = search_laptops(df_laptops, semantic_results, filters)

    print("MESSAGE:", results_dict["message"])
    if results_dict["results"]:
        print("\nTop Results:\n")
        print(format_laptop_results(results_dict["results"]))
    if results_dict["suggestions"]:
        print("\nSuggestions to improve your search:")
        for suggestion in results_dict["suggestions"]:
            print("-", suggestion)


