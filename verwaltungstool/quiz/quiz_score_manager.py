#---------------------------------------------------------------------------------------------------------------------------------------------
# importe <--------------------------<--------------------<--------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------
import json
import os
from verwaltungstool.config import settings
from verwaltungstool.supabase_client import supabase


#---------------------------------------------------------------------------------------------------------------------------------------------
# funtionen <--------------------------<--------------------<--------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------

QUIZ_SCORE_FILE = settings.QUIZ_JSON


def lade_json():
    """Lädt JSON-Daten aus einer Datei."""
    user = supabase.auth.get_user()
    print(user)
    try: 
        response = (supabase.table("quiz_scores")
                    .select("*",count= 'exact')
                    .execute()
                    )

        if response.count == 0:
            response = (supabase.table("quiz_scores")
                        .insert({"user_id" : supabase.auth.get_user().user.id,
                                  "quiz_score_data" : None})
                        .execute()
                        )
            return {} 

        if response.data[0]['quiz_score_data'] == None:
            return {}
        
        return response.data[0]['quiz_score_data']

    except Exception as e:
        print("Fehler: " + e)

    #if os.path.exists(QUIZ_SCORE_FILE):
    #    with open(QUIZ_SCORE_FILE, 'r') as f:
    #       return json.load(f)
    #return {}



def speichere_json(daten):
    """Speichert JSON-Daten in eine Datei."""

    try:
        response = (supabase.table("quiz_scores")
                    .upsert({"user_id" : supabase.auth.get_user().user.id,
                             "quiz_score_data" : daten},
                             on_conflict="user_id")
                    .execute()
                    )
    except Exception as e:
        print("Fehler beim aktualisieren der Quiz Scores:" + e)

    #with open(QUIZ_SCORE_FILE, 'w') as f:
        #json.dump(daten, f, indent=2)

def aktualisiere_frage(name, frage_id, richtig):
    """Aktualisiert den Punktestand für eine bestimmte Frage eines Benutzers."""
    daten = lade_json(QUIZ_SCORE_FILE)
    if name not in daten:# neuer benutzer
        daten[name] = {}
    if frage_id not in daten[name]:# fragen
        daten[name][frage_id] = 0 # initialer punktestand
    if richtig:
        daten[name][frage_id] -= 1# richtige antwort
    else:
        daten[name][frage_id] += 1# falsche antwort
    speichere_json(QUIZ_SCORE_FILE, daten)
    print(f"Aktueller Stand für {name}: {daten[name]}")

if __name__ == "__main__":
    name = input("Name: ")
    frage_id = input("Frage-ID: ")
    antwort = input("Richtig beantwortet? (j/n): ").lower()
    richtig = antwort == 'j'
    aktualisiere_frage(name, frage_id, richtig)
