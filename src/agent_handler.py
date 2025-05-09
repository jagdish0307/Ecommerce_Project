

import os
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain

# Load API key
load_dotenv()
api_key = os.getenv("Groq_Api_Key")

# ✅ Initialize the LLM
llm = ChatOpenAI(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key,
    temperature=0.4
)

# ✅ Define custom system prompt for BuyGenie
system_message = SystemMessagePromptTemplate.from_template(
    "You are BuyGenie, an AI assistant that helps users find the best laptops. "
    "If the question is unrelated to laptops (e.g., mobile phones, greetings), "
    "politely explain that you only assist with laptop-related queries."
)

# Template for user's input
human_message = HumanMessagePromptTemplate.from_template("{input}")

# Combine into a full prompt
chat_prompt = ChatPromptTemplate.from_messages([system_message, human_message])

# ✅ Create LLM chain
llm_chain = LLMChain(llm=llm, prompt=chat_prompt)

# ✅ Final agent interface
def query_assistant(user_input):
    try:
        response = llm_chain.run({"input": user_input})
        return response
    except Exception as e:
        return f"Error: {str(e)}"
