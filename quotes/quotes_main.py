#---------------------------------------------------------------------------------------------------------------------------------------------
#importe <----------------------------<------------------------------<------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------
import sqlite3
import subprocess
#---------------------------------------------------------------------------------------------------------------------------------------------
# funktionen <----------------------------<------------------------------<--------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------
import requests

superbase_base_url = "https://fburyyzzewkdqxutuayl.supabase.co"

Superbaeurl = "https://fburyyzzewkdqxutuayl.supabase.co/rest/v1/quotes?select=text"
API_KEY = ""

HEADER = {
    "apikey": API_KEY,
    "Authorization": f"Bearer {API_KEY}"   
}

def get_quotes():
    api_path = "rest/v1/quotes?select=text"
    api_url = f"{superbase_base_url}/{api_path}"

    """Lädt alle Zitate aus der von Supabase und gibt sie als Liste von Strings zurück."""
    response = requests.get(api_url, headers=HEADER)
    text_list = []
    for row in response.json():
        text_list.append(row['text'])
    return text_list if len(text_list) > 0 else ["Keine Zitate."]

def add_quotes(text, db_path="quotes/quotes.db"):
    """Fügt ein neues Zitat in die SQLite-Datenbank ein."""
    text = text.strip()
    if not text:
        return False
    
    url = f"{superbase_base_url}/rest/v1/quotes"
    inhalt = {
        "text" : text
    }
    
    response = requests.post(url, headers=HEADER, json= inhalt)

    #conn = sqlite3.connect(db_path)
    #cursor = conn.cursor()
    #cursor.execute ("INSERT INTO Zitat (text) VALUES (?)", (text.strip(),))
    #conn.commit()
    #conn.close()
    if not response.ok:
        print("Status: ", response.status_code)
        print("Fehler", response.text)
    return response.ok


def git_pull_quotesdb():
    """Holt die aktuelle quotes.db von Git."""
    try:
        subprocess.run(["git", "pull"], check=True)
        print("Git Pull für quotes.db ausgeführt.")
    except Exception as e:
        print(f"Fehler bei git pull: {e}")

def git_push_quotesdb(commit_message="Update quotes.db"):
    """Pusht die aktuelle quotes.db zu Git."""
    try:
        subprocess.run(["git", "add", "quotes.db"], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push"], check=True)
        print("Git Push für quotes.db ausgeführt.")
    except Exception as e:
        print(f"Fehler bei git push: {e}")

def git_merge_quotesdb():
    """Führt ein git merge aus (z.B. nach Pull)."""
    try:
        subprocess.run(["git", "merge"], check=True)
        print("Git Merge für quotes.db ausgeführt.")
    except Exception as e:
        print(f"Fehler bei git merge: {e}")


