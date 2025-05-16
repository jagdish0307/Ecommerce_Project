# Smart AI-powered laptop recommendation assistant

## 🧠 Problem Statement

Users struggle to find the best laptops matching their budget and specs (e.g., RAM, price). My goal was to build a smart assistant that:

* Understands user queries in natural language
* Filters laptops based on specs (like under ₹50,000 with 8GB RAM)
* Gives intelligent top-2 recommendations
* Supports follow-up questions
* 
## 🎯 Solution: Smart AI-powered laptop recommendation assistant

I built an *AI-powered laptop recommendation assistant*  built using LLMs (Large Language Models) to make laptop shopping intuitive, fast, and personalized. Whether you're a gamer, student, or professional, it  understands your intent and recommends the best options by deeply analyzing your query, product specs, and even your past behavior.
that helps users find the best laptops based on their *budget and specifications*, like price and RAM.

---

## 🚀 Features

* 🔍 **Smart Search Understanding**: Interprets natural language queries like "I want a lightweight laptop for travel" or "Best gaming laptop under 70k" using LLMs.
* 🧠 **LLM-Powered Query Handler**: Maps user queries to technical attributes like weight, GPU, battery life, RAM, etc.
* 📦 **Semantic Product Retrieval**: Embeds product data and performs semantic search using FAISS to retrieve the most relevant items.
* 👤 **Personalized Recommendations**: Learns from user interaction history stored in SQLite and enhances future results.
* 🤖 **Agent Assistant**: Uses a follow-up agent to answer further questions about products, such as "Does this have a backlit keyboard?" or "Which one has the best display?"

---

## 🧱 Tech Stack

| Component       | Technology Used                                    |
| --------------- | -------------------------------------------------- |
| Backend         | Python, Flask                                      |
| Frontend        | Streamlit                                          |
| Vector Search   | FAISS                                              |
| Embeddings      | SentenceTransformers  ('all-MiniLM-L6-v2')                             |
| LLMs            | `gemma-2-9b-it`, `llama-4-scout-17b`, via Groq API |
| Database        | SQLite                                             |
| Version Control | Git, GitHub                                        |

---

## 📂 Project Structure

```
BuyGenie/
│
├── .gitignore
├── .env
├── README.md
├── requirements.txt
├── laptop_prices.csv
├── src/
│   ├── app.py                      # Streamlit app
│   ├── agent_handler.py           # Follow-up LLM agent for user Q&A
│   ├── data_loader.py             # CSV to SQLite loader
│   ├── db/
│   │   ├── laptops.db             # Product database
│   │   └── user_history.db        # User query history
│   ├── embeddings/
│   │   ├── faiss_index.pkl        # FAISS vector store
│   │   ├── id_map.pkl             # ID mapping
│   │   └── laptop_dataframe.pkl   # Product DataFrame
│   ├── llm_query_handler.py       # Maps natural queries to filters
│   ├── llm_recommendation.py      # Converts top items into user-friendly descriptions
│   ├── search_handler.py          # Main handler: query → retrieval → response
│   └── user_history.py            # Stores and fetches user-specific interaction history
```

---

## 🧠 LLM Workflow

1. **Query Understanding (via `llm_query_handler.py`)**:

   * Uses `gemma-2-9b-it` to extract filters like brand, RAM, GPU, use-case, budget, etc.

2. **Semantic Search (via `search_handler.py`)**:

   * Embeds product specs and performs semantic similarity search with FAISS.
  
3. ** Recommendation best for user (via 'recommendation.py')**:

    * it recommends best laptops in detaild description based on search query

4. **Follow-Up Agent (via `agent_handler.py`)**:

   * Uses `llama-4-scout-17b` to answer detailed user queries post-retrieval.

---

## 💡 How BuyGenie Helps Users

* Eliminates the need to manually set filters
* Understands vague and non-technical user requests
* Quickly finds laptops tailored for gaming, travel, office, or editing
* Learns and adapts over time based on past preferences
* Supports intelligent conversations for clarification and comparisons

---

## 🛠️ Setup Instructions

```bash
# 1. Clone the repo
$ git clone https://github.com/jagdish0307/Ecommerce_Project.git
$ cd Ecommerce_Project

# 2. Create virtual environment
$ python -m venv .ecommerce_env
$ source .ecommerce_env/bin/activate  # On Windows: .ecommerce_env\Scripts\activate

# 3. Install dependencies
$ pip install -r requirements.txt

# 4. Set up the environment variables
Create a `.env` file:
GROQ_API_KEY=your_key_here

# 5. Launch the app
$ streamlit run src/app.py
```

---


## 📬 Future Ideas

* Product comparison with images
* Voice-based search
* Daily trending recommendations

---

## 🧑‍💻 Author

**Jagdish**  
💡 Passionate AI Engineer | Creator of BuyGenie  
🔗 [GitHub](https://github.com/jagdish0307)

---

**Enjoy personalized AI laptop shopping with BuyGenie!**

