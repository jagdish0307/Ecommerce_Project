import pandas as pd
import sqlite3
import os



def csv_to_sqlite(csv_path=r'C:\Users\jagdi\BuyGenie Flask-based e-commerce project\laptop_prices.csv', db_path='db/laptops.db'):
    # Create the db directory if it doesn't exist
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Read the CSV file
    df = pd.read_csv(csv_path)

    # Connect to SQLite and write the table
    conn = sqlite3.connect(db_path)
    df.to_sql('laptops', conn, if_exists='replace', index=False)

    print(f"[INFO] Successfully created SQLite DB at: {db_path}")
    conn.close()

if __name__ == "__main__":
    csv_to_sqlite()
