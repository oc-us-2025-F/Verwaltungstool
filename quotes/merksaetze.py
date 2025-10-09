import sqlite3
import time
from datetime import datetime, timedelta

def zitat_main(db_path="Zitat.db"):#<-- Pfad zur SQLite-Datenbank
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT text, created_at From news WHERE datetime(created_at) >= ? ORDER BY datetime(created_at) DESC", (cutoff_date.strftime("%Y-%m-%d %H:%M:%S"),))
    news_items = cursor.fetchall()
    conn.close()
    if not news_items:
        return "noch keine Zitate vorhanden" 
    text = [row[0] for row in news_items]
    time.sleep(60)  # Kurze Pause, um die GUI nicht zu überfordern und es lesbar zu halten
    return "\n\n".join(text)

def add_zitat_item(text, db_path="Zitat.db"):
    if not text.strip():
        return False
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute ("INSERT INTO Zitat (text, created_at) VALUES (?, ?)", (news_text.strip(), created_at))
    conn.commit()
    conn.close()
    return True

