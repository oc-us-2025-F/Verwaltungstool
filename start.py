import sqlite3
import os

# Erstellt die benötigten Datenbanken die ohne personenbezogene daten laufen sollen 
# wird nicht mit ausgelifert damit werden wir die tabelen erstellen und dann diese script in der version 1.0 enfernen sodas keiner mehr darauf zu greifen kann 
#TODO: Tabellen für Merksätze, Counter und Quiz erstellen
#TODO: Funktionen zum Hinzufügen, Löschen und Anzeigen von Einträgen in den jeweiligen Tabellen erstellen
#TODO: Sicherstellen, dass die Datenbanken und Tabellen nur einmal erstellt werden und nicht bei jedem Start des Programms

def create_news_table(db_path="news.db"):# erstellt die news tabelle 
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

def create_mehrsaetze_table(db_path="Zitat.db"):# erstellt die mehrsaetze tabelle
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

def create_counter_table(db_path="Counter.db"):# erstellt die counter tabelle
    pass

def create_quiz_table(db_path="Quiz.db"):# erstellt die quiz tabelle
    pass