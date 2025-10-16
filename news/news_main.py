import sqlite3
from datetime import datetime, timedelta
import subprocess




def get_news(db_path="news/news.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cutoff_date = datetime.now() - timedelta(days=30)
    cursor.execute(
        "SELECT text, created_at FROM news WHERE datetime(created_at) >= ? ORDER BY datetime(created_at) DESC",
        (cutoff_date.strftime("%Y-%m-%d %H:%M:%S"),)
    )
    news_items = cursor.fetchall()
    conn.close()
    return [row[0] for row in news_items] if news_items else ["Keine aktuellen Nachrichten."]

def delete_old_news(db_path="news/news.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cutoff_date = datetime.now() - timedelta(days=30)
    cursor.execute(
        "DELETE FROM news WHERE datetime(created_at) < ?",
        (cutoff_date.strftime("%Y-%m-%d %H:%M:%S"),)
    )
    conn.commit()
    conn.close()

def add_news_item(text, db_path="news/news.db"):
    if not text.strip():
        return False
    if created_at is None:
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute ("INSERT INTO news (text, created_at) VALUES (?, ?)", (news_text.strip(), created_at))
    conn.commit()
    conn.close()
    return True

def git_pull_newsdb():
    """Holt die aktuelle news.db von Git."""
    try:
        subprocess.run(["git", "pull"], check=True)
        print("Git Pull für news.db ausgeführt.")
    except Exception as e:
        print(f"Fehler bei git pull: {e}")

def git_push_newsdb(commit_message="Update news.db"):
    """Pusht die aktuelle news.db zu Git."""
    try:
        subprocess.run(["git", "add", "news.db"], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push"], check=True)
        print("Git Push für news.db ausgeführt.")
    except Exception as e:
        print(f"Fehler bei git push: {e}")

def git_merge_newsdb():
    """Führt ein git merge aus (z.B. nach Pull)."""
    try:
        subprocess.run(["git", "merge"], check=True)
        print("Git Merge für news.db ausgeführt.")
    except Exception as e:
        print(f"Fehler bei git merge: {e}")

