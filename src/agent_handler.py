

import os
import re
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.base import SQLDatabaseToolkit, create_sql_agent
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory

# Load environment variables
load_dotenv()
api_key = os.getenv("Groq_Api_Key")

# Initialize the LLM
llm = ChatOpenAI(
    model="meta-llama/llama-4-scout-17b-16e-instruct",  # or "gemma-2-9b-it"
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key,
    temperature=0.5
)

# Connect to SQLite laptop database
db = SQLDatabase.from_uri("sqlite:///db/laptops.db")

# Create SQL toolkit
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# Initialize memory to retain last 15 messages
memory = ConversationBufferWindowMemory(k=15, return_messages=True)

# Create SQL agent with memory
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=30,
    memory=memory
)

# Helper: Detect comparison intent
def is_compare_query(user_query: str) -> bool:
    keywords = ["compare", "comparison", "vs", "difference", "better", "which one", "vs."]
    return any(k in user_query.lower() for k in keywords)

# Helper: Format raw LLM response for readability
def format_laptop_response(raw_text: str, user_query: str) -> str:
    text = raw_text.strip()
    text = re.sub(r'\n+', '\n', text)
    text = text.replace('•', '\n•')

    if text.startswith('•'):
        text = text[1:].strip()

    if is_compare_query(user_query):
        return text  # Keep bullets for comparisons
    else:
        text = text.replace('•', '-')
        parts = [part.strip() for part in text.split('-') if part.strip()]
        return "\n\n".join(parts)

# Core function to interact with the agent
def query_assistant(user_input: str) -> str:
    try:
        raw_response = agent_executor.run(user_input)
        formatted_response = format_laptop_response(raw_response, user_input)
        return formatted_response
    except Exception as e:
        return f"Error: {str(e)}"

# Main test runner
if __name__ == "__main__":
    print("=" * 80)
    queries = [
        "Show me lightweight laptops with good battery life",
        "Compare Asus Zenbook and Dell XPS models",
        "What are the best laptops for video editing?",
        "List top 3 gaming laptops with 16GB RAM",
        "Which laptop is better: MacBook Pro or Surface Laptop?",
        "Only show me those under 1000 euros",  # memory-aware test
        "Add good webcam and SSD filter",
        "Show only Dell options",
    ]

    for q in queries:
        print(f"\nQuery: {q}\n{'-' * 40}")
        output = query_assistant(q)
        print(output)
        print("=" * 80)


