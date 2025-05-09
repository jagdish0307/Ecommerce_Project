import os
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.base import SQLDatabaseToolkit, create_sql_agent
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory  # ✅ Add memory

# Load environment variables
load_dotenv()
api_key = os.getenv("Groq_Api_Key")

# Initialize the LLM
llm = ChatOpenAI(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key,
    temperature=0.4
)

# Connect to your SQLite database
db = SQLDatabase.from_uri("sqlite:///db/laptops.db")

# Create SQL toolkit
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# ✅ Create a memory object for chat history
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# ✅ Create agent with memory
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    memory=memory  # <<<<< 🧠 memory support here
)

def query_assistant(user_input):
    """
    Executes the assistant agent with memory.
    """
    try:
        response = agent_executor.run(user_input)
        return response
    except Exception as e:
        return f"Error: {str(e)}"

