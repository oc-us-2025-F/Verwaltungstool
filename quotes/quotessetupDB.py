import sqlite3

def create_quotes_db(db_path="quotes/quotes.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Zitat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL        )
    """)
    conn.commit()
    conn.close()
    print(f"DB und Tabelle 'Zitat' wurden (falls nötig) unter '{db_path}' erstellt.")

if __name__ == "__main__":
    create_quotes_db()