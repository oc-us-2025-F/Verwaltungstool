#----------------------------------------------
# --------------> importe  <-------------------
#----------------------------------------------
import json
from datetime import datetime
from collections import Counter
#----------------------------------------------
# ----------------> Pfade  <-------------------
#----------------------------------------------
CLASS_JSON_FILE = "meine_anwesenheit.json"# Pfad zur JSON-Datei mit Anwesenheitsdaten
STATUS_OPTIONS = ["Karlsruhe", "Homeoffice", "Urlaub", "Krankheit", "Feiertag"] #anpassbaare optionen
#----------------------------------------------
# -------------> Functionen  <-----------------
#----------------------------------------------
def load_attendance_data():
    """Lädt die Anwesenheitsdaten aus der JSON-Datei."""
    try:
        with open(CLASS_JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def calculate_monthly_stats(data, year=None, month=None):
    """Berechnet die Anteile pro Status für einen bestimmten Monat."""
    if not data:
        return {}

    # Standard: aktueller Monat
    now = datetime.now() 
    year = year or now.year # hier wird das jahr gesetzt
    month = month or now.month # hier wird der monat gesetzt

    monthly_entries = {
        date: status
        for date, status in data.items() # item = key value paare(date,status)
        if datetime.strptime(date, "%Y-%m-%d").year == year # wenn das jahr und monat passen
        and datetime.strptime(date, "%Y-%m-%d").month == month  # wenn das jahr und monat passen
    }

    if not monthly_entries:# keine einträge
        return {}# leere dict zurückgeben

    counts = Counter(monthly_entries.values()) # zähle vorkommen der status
    total_days = sum(counts.values()) # gesamtanzahl der tage im monat

    stats = {
        status: {
            "tage": counts.get(status, 0),
            "quote": round((counts.get(status, 0) / total_days) * 100, 1) # prozentualer anteil
        }
        for status in STATUS_OPTIONS # für jeden status in den optionen
    }

    return stats # zurückgeben wird das dict mit den stats

def print_monthly_overview(stats, year=None, month=None):
    """Gibt eine einfache Übersicht in der Konsole aus."""
    if not stats:
        print("Keine Einträge für diesen Monat gefunden.")#falls keine einträge da ist
        return 

    now = datetime.now() # standard aktueller monat und jahr
    year = year or now.year
    month = month or now.month

    print(f"\n📅 Anwesenheitsübersicht ({month:02d}/{year})")# ausgabe der übersicht
    for status, values in stats.items():
        print(f"{status:12}: {values['tage']} Tage ({values['quote']} %)")