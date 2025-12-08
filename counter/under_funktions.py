import sqlite3
from datetime import date

DB_PATH = "stoerungen.db"
# Wichtig: Wir behalten den Tippfehler "algemein" bei, damit er zu den Button-Texten passt.
ARTEN_DER_STOERUNG = ["technisch", "algemein"] 

def _connect():
    """Hilfsfunktion zur Herstellung der Datenbankverbindung."""
    return sqlite3.connect(DB_PATH)

def update_counter(art):
    """
    Erhöht den Zähler für die angegebene Störungsart für das heutige Datum.
    Wird bei Klick auf einen Button in der GUI aufgerufen.
    
    Da ensure_today_exists entfernt wurde, enthält diese Funktion die 
    notwendige Sicherheitsabfrage, um den Eintrag mit 0 zu erstellen, 
    bevor er erhöht wird (INSERT OR IGNORE).
    """
    heute = date.today().isoformat()
    conn = _connect()
    c = conn.cursor()
    c.execute("""
        INSERT OR IGNORE INTO counter (Art_der_störung, value, datum) 
        VALUES (?, 0, ?)
    """, (art, heute))
    
    # Erhöht den Wert um 1
    c.execute("""
        UPDATE counter SET value = value + 1 
        WHERE Art_der_störung = ? AND datum = ?
    """, (art, heute))
    
    conn.commit()
    conn.close()

def get_counter(art):
    """Gibt den Zählerstand für eine Störungsart heute zurück."""
    heute = date.today().isoformat()
    conn = _connect()
    c = conn.cursor()
    c.execute("SELECT value FROM counter WHERE Art_der_störung = ? AND datum = ?", (art, heute))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 0

def get_counter_total():
    """Gibt den Gesamt-Zählerstand für alle Arten heute zurück."""
    heute = date.today().isoformat()
    conn = _connect()
    c = conn.cursor()
    c.execute("SELECT SUM(value) FROM counter WHERE datum = ?", (heute,))
    result = c.fetchone()
    conn.close()
    return result[0] if result and result[0] is not None else 0

def get_counter_display_text():
    """Formatiert den Text für die GUI-Anzeige."""
    tech_count = get_counter("technisch")
    general_count = get_counter("algemein")
    total = get_counter_total()
    
    return (
        f"Zählerstände von heute ({date.today().strftime('%d.%m.%Y')}):\n"
        f"Technisch: {tech_count} | Allgemein: {general_count}\n"
        f"Gesamt: {total}"
    )
