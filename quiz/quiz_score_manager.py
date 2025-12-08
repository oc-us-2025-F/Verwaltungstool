#---------------------------------------------------------------------------------------------------------------------------------------------
# importe <--------------------------<--------------------<--------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------
import json
import os

#---------------------------------------------------------------------------------------------------------------------------------------------
# funtionen <--------------------------<--------------------<--------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------


def lade_json(dateiname):
    """Lädt JSON-Daten aus einer Datei."""
    if os.path.exists(dateiname):
        with open(dateiname, 'r') as f:
            return json.load(f)
    return {}

def speichere_json(dateiname, daten):
    """Speichert JSON-Daten in eine Datei."""
    with open(dateiname, 'w') as f:
        json.dump(daten, f, indent=2)

def aktualisiere_frage(name, frage_id, richtig, dateiname='quiz_scores.json'):
    """Aktualisiert den Punktestand für eine bestimmte Frage eines Benutzers."""
    daten = lade_json(dateiname)
    if name not in daten:# neuer benutzer
        daten[name] = {}
    if frage_id not in daten[name]:# fragen
        daten[name][frage_id] = 0 # initialer punktestand
    if richtig:
        daten[name][frage_id] -= 1# richtige antwort
    else:
        daten[name][frage_id] += 1# falsche antwort
    speichere_json(dateiname, daten)
    print(f"Aktueller Stand für {name}: {daten[name]}")

if __name__ == "__main__":
    name = input("Name: ")
    frage_id = input("Frage-ID: ")
    antwort = input("Richtig beantwortet? (j/n): ").lower()
    richtig = antwort == 'j'
    aktualisiere_frage(name, frage_id, richtig)
