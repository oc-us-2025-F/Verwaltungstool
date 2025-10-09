import sqlite3
from datetime import date

DB_PATH = "stoerungen.db"

def commit_and_close(conn):
    """
    Commit und close für die SQLite-Datenbankverbindung.
    Diese Funktion wird verwendet, um Änderungen in der Datenbank zu speichern    
    """
    conn.commit()
    conn.close()

def init_db():
    """
    Initialisiert die SQLite-Datenbank und erstellt die Tabelle für den Störungs-Counter.
    Diese Funktion wird beim Start des Programms aufgerufen, um sicherzustellen,
    dass die Datenbank und die erforderlichen Tabellen vorhanden sind.
    Wenn die Tabelle bereits existiert, wird sie nicht erneut erstellt.
    Außerdem werden die beiden Störungstypen "technisch" und "algemein
    mit einem Startwert von 0 für das heutige Datum in die Tabelle eingefügt,
    falls sie noch nicht vorhanden sind.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS counter (
            Art_der_störung TEXT,
            value INTEGER NOT NULL,
            datum TEXT NOT NULL,
            PRIMARY KEY (Art_der_störung, datum)
        )
    """)
    for Art_der_störung in ["technisch", "algemein"]:
        c.execute(
            "INSERT OR IGNORE INTO counter (Art_der_störung, value, datum) VALUES (?, ?, ?)",
            (Art_der_störung, 0, date.today().isoformat())
        )
    commit_and_close(conn)

def get_counter(Art_der_störung):
    """
    Gibt den aktuellen Zählerstand für die angegebene Art der Störung zurück.
    Diese Funktion wird verwendet, um die Anzahl der Störungen für einen bestimmten Typ
    zu ermitteln. Sie prüft die Datenbank auf den aktuellen Zählerstand für den
    angegebenen Störungstyp und das heutige Datum. Wenn kein Eintrag gefunden wird
    oder der Wert None ist, wird 0 zurückgegeben.
    Args:
        Art_der_störung (str): Der Typ der Störung, für den der Zählerstand abgefragt wird.
    Returns:
        int: Der aktuelle Zählerstand für die angegebene Art der Störung.
    """
    heute = date.today().isoformat()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT SUM(value) FROM counter WHERE Art_der_störung = ? AND datum = ?",
        (Art_der_störung, heute)
    )
    result = c.fetchone()
    conn.close()
    return result[0] if result and result[0] is not None else 0

def get_counter_total(Art_der_störung):
    """
    Gibt den Gesamtzählerstand für die angegebene Art der Störung zurück.
    Diese Funktion wird verwendet, um die Gesamtanzahl der Störungen für einen bestimmten Typ
    zu ermitteln, unabhängig vom Datum. Sie prüft die Datenbank auf alle Einträge
    für den angegebenen Störungstyp und summiert die Werte. Wenn kein Eintrag gefunden wird
    oder der Wert None ist, wird 0 zurückgegeben.
    Args:
        Art_der_störung (str): Der Typ der Störung, für den der Gesamtzählerstand abgefragt wird.
    Returns:
        int: Der Gesamtzählerstand für die angegebene Art der Störung.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT SUM(value) FROM counter WHERE Art_der_störung = ?",
        (Art_der_störung,)
    )
    result = c.fetchone()
    conn.close()
    return result[0] if result and result[0] is not None else 0

def update_counter(Art_der_störung):
    """
    Aktualisiert den Zähler für die angegebene Art der Störung.
    Diese Funktion wird verwendet, um den Zählerstand für einen bestimmten Störungstyp
    zu erhöhen. Sie prüft, ob ein Eintrag für den heutigen Tag und den angegebenen Störungstyp
    bereits existiert. Wenn nicht, wird ein neuer Eintrag mit einem Startwert von 0 erstellt.
    Anschließend wird der Zählerstand um 1 erhöht.
    Args:
        Art_der_störung (str): Der Typ der Störung, dessen Zähler aktualisiert werden soll.
    """
    heute = date.today().isoformat()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT OR IGNORE INTO counter (Art_der_störung, value, datum) VALUES (?, ?, ?)",
        (Art_der_störung, 0, heute)
    )
    c.execute(
        "UPDATE counter SET value = value + 1 WHERE Art_der_störung = ? AND datum = ?",
        (Art_der_störung, heute)
    )
    commit_and_close(conn)

def update_labels(counter_label, gesamt=False):
    """
    Aktualisiert die Anzeige der Zählerstände in der GUI.
    Diese Funktion wird verwendet, um die aktuellen Zählerstände für die Störungstypen
    "technisch" und "algemein" in der GUI anzuzeigen. Sie ruft die aktuellen Zählerstände
    und die Gesamtzählerstände (falls gewünscht) aus der Datenbank ab und aktualisiert
    das Label in der GUI entsprechend.
    Args:
        counter_label (tk.Label): Das Label-Widget in der GUI, das die Zählerstände anzeigt.
        gesamt (bool): Optional. Wenn True, werden die Gesamtzählerstände angezeigt.
                       Standardmäßig ist dieser Parameter False.
    """
    technisch = get_counter("technisch")
    algemein = get_counter("algemein")
    if gesamt:
        technisch_total = get_counter_total("technisch")
        algemein_total = get_counter_total("algemein")
        counter_label.config(
            text=f"Technisch: {technisch} (Gesamt: {technisch_total})   Allgemein: {algemein} (Gesamt: {algemein_total})"
        )
    else:
        counter_label.config(
            text=f"Technisch: {technisch}   Allgemein: {algemein}"
        )

def get_counter_display_text():
    """
    Erzeugt den formatierten Textstring für das PySide6/Qt Label.
    Verwendet die Zähler für heute und die Gesamtzahlen (wie im Original-Code).
    Returns:
        str: Der formatierte Text, z.B. "Gesamt: 15 | Technisch: 10 | Allgemein: 5"
    """
    technisch = get_counter("technisch")
    algemein = get_counter("algemein")
    
    # Wir nutzen die get_counter_total Funktion
    technisch_total = get_counter_total("technisch")
    algemein_total = get_counter_total("algemein")
    
    total_heute = technisch + algemein
    total_gesamt = technisch_total + algemein_total
    
    return (
        f"Gesamt (Heute): {total_heute} | Gesamt (Alle Zeit): {total_gesamt}\n"
        f"Technisch (Heute): {technisch} (Gesamt: {technisch_total}) | "
        f"Allgemein (Heute): {algemein} (Gesamt: {algemein_total})"
    )


        