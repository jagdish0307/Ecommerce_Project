
import streamlit as st
import pandas as pd
import sqlite3
from search_handler import search_laptops
from user_history import save_history_to_db, get_user_history
from agent_handler import query_assistant
from llm_recommendation import generate_recommendation
from llm_query_handler import understand_query
from vector_store import fetch_laptop_data

# Static user ID
user_id = "user123"

# Cache laptop data loading to avoid repeated I/O
@st.cache_data(show_spinner=False)
def load_laptop_data():
    return fetch_laptop_data()

df_laptops = load_laptop_data()

# Streamlit UI setup
st.set_page_config(page_title="BuyGenie - AI Laptop Finder", layout="wide")
st.title("💻 BuyGenie")
st.caption("Your personal AI-powered laptop shopping assistant.")

# Sidebar input
with st.sidebar:
    st.header("🔍 Laptop Query")
    user_query = st.text_input("Describe what you want in a laptop:", "")

# Remove incorrect early search call
# (We will do search inside Tab 1)

# Tabs: Search | Recommendation | Assistant | History
tab1, tab2, tab3, tab4 = st.tabs(["🔎 Search", "🧠 Recommendation", "🧞 Assistant", "📜 History"])

# ---------------- Tab 1: Search ----------------
with tab1:
    st.subheader("Matching Laptops")
    if user_query:
        try:
            # Extract structured filters from user query
            filters = understand_query(user_query)

            # Semantic search results empty for now or replace with your vector search results
            semantic_results = []

            # Run combined semantic + structured filtering search
            results_dict = search_laptops(df_laptops, semantic_results, filters)

            if results_dict["results"]:
                for idx, laptop in enumerate(results_dict["results"], 1):
                    st.markdown(f"""
                    **{idx}. {laptop['Company']} {laptop['Product']}**
                    - 💾 RAM: {laptop['Ram']} GB
                    - 💽 Storage: {laptop['PrimaryStorage']} GB
                    - ⚖️ Weight: {laptop['Weight']} kg
                    - 💰 Price: €{laptop['Price_euros']}
                    """)
            else:
                st.warning(results_dict["message"])
                if results_dict["suggestions"]:
                    st.info("Suggestions to improve your search:")
                    for s in results_dict["suggestions"]:
                        st.markdown(f"- {s}")

        except Exception as e:
            st.error(f"Error during search: {str(e)}")
    else:
        st.info("Please enter a query in the sidebar.")

# ---------------- Tab 2: Recommendation ----------------
with tab2:
    st.subheader("📢 LLM-Powered Recommendation")
    if user_query:
        try:
            # Use a small subset of laptops for generating recommendations
            conn = sqlite3.connect("db/laptops.db")
            df_subset = pd.read_sql_query("SELECT * FROM laptops LIMIT 3", conn)
            conn.close()

            with st.spinner("Thinking... 🤖"):
                recommendation = generate_recommendation(user_query, df_subset)

            # Save to history DB
            save_history_to_db([
                {
                    "user_id": user_id,
                    "query": user_query,
                    "recommendation": recommendation
                }
            ])

            st.success("Here's my advice:")
            st.markdown(f"```markdown\n{recommendation}\n```")
        except Exception as e:
            st.error(f"⚠️ Error generating recommendation: {str(e)}")
    else:
        st.info("Please enter a query in the sidebar first.")

# ---------------- Tab 3: Assistant ----------------
with tab3:
    st.subheader("🧞 Ask the Laptop Assistant")
    st.write("Ask about brands, specs, cheapest laptops, GPU types, etc.")

    if "agent_messages" not in st.session_state:
        st.session_state.agent_messages = [
            {"role": "assistant", "content": "👋 Hi! I'm your laptop assistant. Ask me anything about laptops!"}
        ]

    for msg in st.session_state.agent_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask me anything...")

    if user_input:
        st.session_state.agent_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.spinner("Thinking..."):
            response = query_assistant(user_input)

        st.session_state.agent_messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            if "I only help with laptops" in response or "can't help" in response:
                st.info(response)
            elif "something went wrong" in response:
                st.error(response)
            else:
                st.markdown(response)

# ---------------- Tab 4: History ----------------
with tab4:
    st.subheader("🕓 Your Query History")
    history = get_user_history(user_id)
    if history:
        for q, r, ts in history:
            st.markdown(f"- ⏱️ {ts} | **Query**: _{q}_ \n**Recommendation**: _{r}_")
    else:
        st.info("No previous queries found.")
