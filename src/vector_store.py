


import os
import sqlite3
import pickle
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer

# Configs
DB_PATH = 'db/laptops.db'
TABLE_NAME = 'laptops'

INDEX_SAVE_PATH = 'embeddings/faiss.index'
DF_SAVE_PATH = 'embeddings/laptop_dataframe.pkl'
ID_MAP_SAVE_PATH = 'embeddings/id_map.pkl'
EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2'

# Initialize embedding model once for reuse
embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

def fetch_laptop_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME}", conn)
    conn.close()
    return df

def create_embedding_text(row):
    return (
        f"{row['Company']} {row['Product']} {row['TypeName']} {row['Inches']} inch, "
        f"{row['Ram']} RAM, {row['OS']}, {row['Weight']}kg, {row['Screen']} "
        f"{row['ScreenW']}x{row['ScreenH']}, Touchscreen: {row['Touchscreen']}, "
        f"IPS: {row['IPSpanel']}, Retina: {row['RetinaDisplay']}, "
        f"{row['CPU_company']} {row['CPU_model']} @ {row['CPU_freq']}GHz, "
        f"{row['PrimaryStorage']} {row['PrimaryStorageType']}, "
        f"{row['SecondaryStorage']} {row['SecondaryStorageType']}, "
        f"{row['GPU_company']} {row['GPU_model']}, Price: {row['Price_euros']} euros"
    )

def generate_embeddings(texts):
    embeddings = embedding_model.encode(texts, convert_to_numpy=True).astype('float32')
    return embeddings

def save_index(index):
    os.makedirs(os.path.dirname(INDEX_SAVE_PATH), exist_ok=True)
    faiss.write_index(index, INDEX_SAVE_PATH)

def save_dataframe(df):
    df.to_pickle(DF_SAVE_PATH)

def save_id_map(df):
    id_map = {i: int(df.iloc[i].name) for i in range(len(df))}
    with open(ID_MAP_SAVE_PATH, 'wb') as f:
        pickle.dump(id_map, f)

def build_faiss_index():
    print("[INFO] Fetching laptop data...")
    df = fetch_laptop_data()
    df.reset_index(drop=True, inplace=True)  # Ensure clean indexing

    print("[INFO] Creating text for embeddings...")
    texts = df.apply(create_embedding_text, axis=1).tolist()

    print("[INFO] Generating embeddings...")
    embeddings = generate_embeddings(texts)
    print(f"[INFO] Generated {embeddings.shape[0]} embeddings of dim {embeddings.shape[1]}")

    print("[INFO] Building FAISS index...")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    save_index(index)
    save_dataframe(df)
    save_id_map(df)

    print(f"[INFO] FAISS index saved at {INDEX_SAVE_PATH}")
    print(f"[INFO] DataFrame saved at {DF_SAVE_PATH}")
    print(f"[INFO] ID map saved at {ID_MAP_SAVE_PATH}")

# ==== New helper functions to load and use the index and embeddings ====

def get_faiss_index():
    if not os.path.exists(INDEX_SAVE_PATH):
        raise FileNotFoundError(f"FAISS index not found at {INDEX_SAVE_PATH}")
    index = faiss.read_index(INDEX_SAVE_PATH)
    return index

def get_id_map():
    if not os.path.exists(ID_MAP_SAVE_PATH):
        raise FileNotFoundError(f"ID map not found at {ID_MAP_SAVE_PATH}")
    with open(ID_MAP_SAVE_PATH, "rb") as f:
        id_map = pickle.load(f)
    return id_map

def get_embeddings(text: str):
    embedding = embedding_model.encode(text, convert_to_numpy=True).astype('float32')
    return embedding

if __name__ == "__main__":
    build_faiss_index()

