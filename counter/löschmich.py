import sqlite3
import os
from datetime import date

DB_PATH = os.path.join(os.path.dirname(__file__),"stoerungen.db")

def init_db():
    """
    Initialisiert die SQLite-Datenbank und stellt sicher, dass die Tabelle existiert.
    Wird beim Start des Programms aufgerufen.
    """
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
        -- Primärschlüssel aus Störungsart und Datum verhindert Duplikate am selben Tag
        CREATE TABLE IF NOT EXISTS counter (
            Art_der_störung TEXT,
            value INTEGER NOT NULL,
            datum TEXT NOT NULL,
            PRIMARY KEY (Art_der_störung, datum)
        )
    """)
    print("Datenbank initialisiert.")



init_db() 