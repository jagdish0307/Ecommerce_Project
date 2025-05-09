import sqlite3
from datetime import datetime

# Initialize the history table if not exists
def init_history_db(db_path="db/user_history.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            query TEXT,
            product_name TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

# Save a search record
def log_user_interaction(user_id, query, product_name, db_path="db/user_history.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO history (user_id, query, product_name, timestamp)
        VALUES (?, ?, ?, ?)
    """, (user_id, query, product_name, datetime.now().isoformat()))
    conn.commit()
    conn.close()

# Retrieve user history
def get_user_history(user_id, db_path="db/user_history.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT query, product_name, timestamp FROM history
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT 20
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# For testing
if __name__ == "__main__":
    init_history_db()
    log_user_interaction("user123", "Find budget gaming laptops", "Dell Inspiron GTX 1650")
    log_user_interaction("user123", "Best laptops for editing", "HP Envy RTX 3050")
    history = get_user_history("user123")
    for row in history:
        print(row)
