
import os
import json
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_groq import ChatGroq
from langchain_core.runnables import Runnable

load_dotenv()
groq_api_key = os.getenv("Groq_Api_Key")

# Initialize the Groq LLM
llm = ChatGroq(
    api_key=groq_api_key,
    model="llama3-8b-8192",  #"meta-llama/llama-4-scout-17b-16e-instruct",
    temperature=0
)

# Use JSON parser for strict output formatting
parser = JsonOutputParser()

# Define prompt template with instructions and formatting
prompt = PromptTemplate.from_template("""
You are a smart laptop recommendation assistant.

Your job is to extract structured filters from the user query and return them strictly in the following JSON format:

{{
  "brand": null,
  "model": null,
  "use_case": null,
  "price_above": null,
  "price_under": null,
  "ram_above": null,
  "ram_below": null,
  "storage_above": null,
  "storage_below": null,
  "weight_above": null,
  "weight_under": null
}}

Only return JSON. No explanation. Do not include units (like GB or kg) in the values.

User Query: "{query}"
""")

# Chain it all together
query_chain: Runnable = prompt | llm | parser

# Callable function
def understand_query(user_query: str) -> dict:
    try:
        return query_chain.invoke({"query": user_query})
    except Exception as e:
        print(f"Error: {e}")
        return {
            "brand": None,
            "model": None,
            "use_case": None,
            "price_above": None,
            "price_under": None,
            "ram_above": None,
            "ram_below": None,
            "storage_above": None,
            "storage_below": None,
            "weight_above": None,
            "weight_under": None
        }

# Example test
if __name__ == "__main__":
    sample_queries = [
        "I want a Dell laptop with 16GB RAM under 800 euros",
        "Find a gaming laptop with at least 32GB RAM",
        "Show me a lightweight HP laptop for students",
        "Suggest a laptop for remote work under 1.5kg",
        "Need a MacBook for office use under €1000",
        "Above 8GB RAM and below 700 euro"
    ]
    for q in sample_queries:
        print("="*60)
        print(f"Query: {q}")
        response = understand_query(q)
        print("Parsed Output:")
        print(json.dumps(response, indent=2))

