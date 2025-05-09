import os
from dotenv import load_dotenv
from openai import OpenAI

# Load Groq API key
load_dotenv()
api_key = os.getenv("Groq_Api_Key")

# Groq LLM setup
client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)
MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"

def generate_recommendation(user_query, products_df):
    if products_df.empty:
        return "Sorry, I couldn't find any laptops matching your request."

    # Format products for the prompt
    product_lines = []
    for _, row in products_df.iterrows():
        line = f"- {row['Company']} {row['Product']}, {row['Ram']}GB RAM, {row['PrimaryStorage']}GB {row['PrimaryStorageType']}, {row['GPU_model']} GPU, €{row['Price_euros']}, Weight: {row['Weight']}kg"
        product_lines.append(line)

    product_list = "\n".join(product_lines)

    prompt = f"""
You are a tech shopping assistant. A user asked: "{user_query}"

Here are the matching laptops:
{product_list}

Write a helpful natural language recommendation for the user. Focus on the top 2-3 options. Mention highlights like performance, price, portability, or use-case fit (gaming, office, school, etc). Be concise and helpful.
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a tech expert who helps users choose laptops."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )

    return response.choices[0].message.content.strip()

# Example usage (you can test manually here):
if __name__ == "__main__":
    import pandas as pd
    from sqlite3 import connect

    # Load 3 laptops from DB for test
    conn = connect("db/laptops.db")
    test_df = pd.read_sql_query("SELECT * FROM laptops LIMIT 3", conn)
    conn.close()

    user_query = "best laptops for Gamming which weights under 1.5kg"
    print(generate_recommendation(user_query, test_df))
