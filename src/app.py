# app.py

import streamlit as st
import pandas as pd
import sqlite3
from search_handler import search_laptops
from user_history import log_user_interaction, get_user_history
from agent_handler import query_assistant
from llm_recommendation import generate_recommendation

# Static user ID
user_id = "user123"

# Streamlit UI setup
st.set_page_config(page_title="BuyGenie - AI Laptop Finder", layout="wide")
st.title("💻 BuyGenie")
st.caption("Your personal AI-powered laptop shopping assistant.")

# Sidebar input
with st.sidebar:
    st.header("🔍 Laptop Query")
    user_query = st.text_input("Describe what you want in a laptop:", "")

# Run search if input exists
search_results = None
if user_query:
    log_user_interaction(user_id, user_query, "", db_path="db/user_history.db")
    search_results = search_laptops(user_query)

# Tabs: Search | Recommendation | Assistant | History
tab1, tab2, tab3, tab4 = st.tabs(["🔎 Search", "🧠 Recommendation", "🧞 Assistant", "📜 History"])

# ---------------- Tab 1: Search ----------------
with tab1:
    st.subheader("Matching Laptops")
    if user_query:
        if isinstance(search_results, str):
            st.error(search_results)
        elif not search_results.empty:
            for idx, (_, row) in enumerate(search_results.iterrows()):
                st.markdown(f"""
                **{idx+1}. {row['Company']} {row['Product']}**
                - 💾 RAM: {row['Ram']}GB | 💽 {row['PrimaryStorage']}GB {row['PrimaryStorageType']}
                - 🎮 GPU: {row['GPU_model']} | 💰 Price: €{row['Price_euros']} | ⚖️ {row['Weight']}kg
                """)
        else:
            st.warning("No laptops found for that query.")
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
            {"role": "assistant", "content": "Hi! I'm your laptop assistant. Ask me anything."}
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
            st.markdown(response)

# ---------------- Tab 4: History ----------------
with tab4:
    st.subheader("🕓 Your Query History")
    history = get_user_history(user_id)
    if history:
        for q, p, ts in history:
            st.markdown(f"- ⏱️ {ts} | **Query**: _{q}_")
    else:
        st.info("No previous queries found.")


# import streamlit as st
# from agent_handler import query_assistant

# st.set_page_config(page_title="BuyGenie Assistant", layout="wide")

# st.title("🧞‍♂️ BuyGenie Laptop Assistant")
# st.write("Ask me anything about our laptops — recommendations, specs, counts, or comparisons!")

# # Session state for chat
# if "messages" not in st.session_state:
#     st.session_state.messages = [
#         {"role": "assistant", "content": "Hi! How can I assist you with laptops today?"}
#     ]

# # Display chat history
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# # User input
# user_input = st.chat_input("Type your laptop-related question here...")

# if user_input:
#     # Display user message
#     st.session_state.messages.append({"role": "user", "content": user_input})
#     with st.chat_message("user"):
#         st.markdown(user_input)

#     # Get agent response
#     with st.spinner("Thinking..."):
#         response = query_assistant(user_input)

#     # Display assistant message
#     st.session_state.messages.append({"role": "assistant", "content": response})
#     with st.chat_message("assistant"):
#         st.markdown(response)
