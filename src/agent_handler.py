

import os
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.base import SQLDatabaseToolkit, create_sql_agent
from langchain_openai import ChatOpenAI


# Load environment variables
load_dotenv()
api_key = os.getenv("Groq_Api_Key")


llm = ChatOpenAI(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key,
    temperature=0.4
)

# Connect to your SQLite database (adjust path if needed)
db = SQLDatabase.from_uri("sqlite:///db/laptops.db")

# Create Toolkit and Agent
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent_executor = create_sql_agent(llm=llm, toolkit=toolkit, verbose=True)

def query_assistant(user_input):
    """
    Executes the assistant agent with the given user input.
    """
    try:
        response = agent_executor.run(user_input)
        return response
    except Exception as e:
        return f"Error: {str(e)}"

