# BuyGenie: AI-Powered Laptop Recommendation System

BuyGenie is an AI-powered e-commerce recommendation system that provides smart, personalized laptop suggestions based on user queries. It uses LLMs, semantic search, and SQLite to deliver accurate and relevant results. The system understands user intent, applies post-filtering, and gives recommendations tailored to user preferences.

---

## 🚀 Features

* 🧠 **LLM Query Understanding:** Interprets natural language queries like "best gaming laptop under ₹80,000" using `gemma-2-9b-it` (via Groq API).
* 🔍 **Semantic Search:** Retrieves similar laptop records using vector embeddings (FAISS).
* 🧾 **Post-Filtering:** Filters results by price, weight, RAM, GPU, etc.
* 💡 **Personalized Recommendations:** Adapts based on user history (stored in SQLite).
* 🤖 **LLM Agent:** Handles follow-up questions and acts as a chatbot interface.
* 📊 **Streamlit UI:** Simple and intuitive frontend for users to interact.

---

## 🗂️ Project Structure

```
BuyGenie Flask-based e-commerce project/
│
├── .ecommerce_env/                 # Virtual environment (ignored by git)
├── .env                            # Stores Groq API key (ignored by git)
├── .gitignore                      # Specifies untracked files
├── laptop_prices.csv              # Raw data (ignored by git)
├── flipkart_data.csv              # Optional data file (ignored by git)
├── flipkart_cleaned_data.csv      # Cleaned data (ignored by git)
├── requirements.txt               # Python dependencies
├── src/
│   ├── app.py                      # Streamlit application
│   ├── data_loader.py             # Loads CSV to SQLite
│   ├── db/
│   │   ├── laptops.db             # Main product DB (ignored by git)
│   │   └── user_history.db        # User interaction DB (ignored by git)
│   ├── embeddings/
│   │   ├── faiss_index.pkl        # FAISS index (ignored by git)
│   │   ├── id_map.pkl             # ID mappings (ignored by git)
│   │   └── laptop_dataframe.pkl   # Dataframe pickle (ignored by git)
│   ├── llm_query_handler.py       # Handles query understanding
│   ├── llm_recommendation.py      # Formats natural language recommendations
│   ├── personalized_recommender.py# Uses user history to refine suggestions
│   ├── rag_pipeline.py            # Combines LLM, FAISS, DB
│   ├── search_handler.py          # Semantic search with filtering
│   ├── user_history.py            # Saves/retrieves user query history
│   └── vector_store.py            # FAISS vector store operations
└── testing.ipynb                  # Development/test notebook
```

---

## 🔧 Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/jagdish0307/Ecommerce_Project.git
cd Ecommerce_Project
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv .ecommerce_env
.ecommerce_env\Scripts\activate    # Windows
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Add `.env` File with Groq API Key

```
Groq_Api_Key=your_groq_api_key_here
```

---

## 🧪 Run the App

```bash
streamlit run src/app.py
```

---

## ⚙️ Git Setup Tips

* Ignore unnecessary files using `.gitignore`:

```
.ecommerce_env/
__pycache__/
.env
src/db/
src/embeddings/
*.csv
```

* Git Large File Support (.gitattributes is optional): Use [Git LFS](https://git-lfs.github.com/) for files >50MB.

---

## 📌 Notes

* FAISS index and database files are ignored to avoid large Git pushes.
* Ensure Groq API key is stored securely in `.env`.
* Use SQLite for storing both product data and user interaction history.
* LLM model used: `gemma-2-9b-it` via [Groq API](https://console.groq.com/).

---

## 📬 Future Enhancements

* Add product images and rich cards in Streamlit
* Improve multi-turn conversations with memory
* Expand support for other product categories

---

## 🧑‍💻 Author

**Jagdish Patil**
GitHub: [@jagdish0307](https://github.com/jagdish0307)

---

## 📄 License

This project is licensed under the MIT License.
