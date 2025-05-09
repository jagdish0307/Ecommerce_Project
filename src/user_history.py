# import sqlite3
# from datetime import datetime

# # Function to check if a column exists in a table
# def column_exists(conn, table, column):
#     cursor = conn.cursor()
#     cursor.execute(f"PRAGMA table_info({table})")
#     columns = cursor.fetchall()
#     return any(col[1] == column for col in columns)

# # Initialize the history table if not exists
# def init_history_db(db_path="db/user_history.db"):
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()
    
#     # Create table if not exists
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS history (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             user_id TEXT NOT NULL,
#             query TEXT,
#             product_name TEXT,
#             product_details TEXT,
#             recommendation TEXT,  -- New column for recommendation
#             timestamp TEXT
#         )
#     """)

#     # Check if the 'recommendation' column exists, if not add it
#     if not column_exists(conn, 'history', 'recommendation'):
#         cursor.execute("ALTER TABLE history ADD COLUMN recommendation TEXT")
    
#     conn.commit()
#     conn.close()


# # Save a query and its recommendation
# def log_user_interaction(user_id, query, product_name, product_details, recommendation, db_path="db/user_history.db"):
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()
#     cursor.execute("""
#         INSERT INTO history (user_id, query, product_name, product_details, recommendation, timestamp)
#         VALUES (?, ?, ?, ?, ?, ?)
#     """, (user_id, query, product_name, product_details, recommendation, datetime.now().isoformat()))
#     conn.commit()
#     conn.close()

# # Retrieve recent history for a user
# def get_user_history(user_id, db_path="db/user_history.db"):
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()
#     cursor.execute("""
#         SELECT query, recommendation, timestamp FROM history
#         WHERE user_id = ?
#         ORDER BY timestamp DESC
#         LIMIT 20
#     """, (user_id,))
#     rows = cursor.fetchall()
#     conn.close()
#     return rows

# # For testing
# if __name__ == "__main__":
#     init_history_db()
#     log_user_interaction("user123", "Best laptop under $1000", "Try the Acer Nitro 5 with i5, RTX 3050, 16GB RAM.", "This is a great recommendation for gaming and performance.")
#     history = get_user_history("user123")
#     for row in history:
#         print(row)
import sqlite3
from datetime import datetime

def ensure_column_exists(cursor, table, column, column_type):
    cursor.execute(f"PRAGMA table_info({table})")
    columns = [info[1] for info in cursor.fetchall()]
    if column not in columns:
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {column_type}")

def save_history_to_db(history, db_path="db/user_history.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Step 1: Ensure table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            query TEXT,
            timestamp TEXT
        )
    """)

    # Step 2: Ensure 'recommendation' column exists
    ensure_column_exists(cursor, "history", "recommendation", "TEXT")

    # Step 3: Insert entries
    for entry in history:
        cursor.execute("""
            INSERT INTO history (user_id, query, recommendation, timestamp)
            VALUES (?, ?, ?, ?)
        """, (
            entry.get("user_id", "unknown"),
            entry.get("query", ""),
            entry.get("recommendation", ""),
            datetime.now().isoformat()
        ))

    conn.commit()
    conn.close()

def get_user_history(user_id, db_path="db/user_history.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT query, recommendation, timestamp
        FROM history
        WHERE user_id = ?
        ORDER BY timestamp DESC
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()
    return rows

# Test saving and retrieving
if __name__ == "__main__":
    sample_history = [
        {"user_id": "user123", "query": "Best gaming laptop", "recommendation": "Try Acer Nitro 5"},
        {"user_id": "user123", "query": "Lightweight laptop for students", "recommendation": "Consider Dell XPS 13"}
    ]
    save_history_to_db(sample_history)
    print(get_user_history("user123"))
