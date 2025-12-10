import subprocess
import os

DB_PATH = "quiz_app.sqlite"

def git_pull_db():
    """Führt einen Git Pull für die Datenbank durch.
    Diese Funktion wird verwendet, um die neuesten Änderungen aus dem Git-Repository
    zu ziehen, in dem die Datenbank gespeichert ist.
    Sie geht davon aus, dass die Datenbank in einem Git-Repository verwaltet wird.
    """
    print("git pull im quiz läuft")
    db_abspath = os.path.abspath(DB_PATH)
    db_dir = os.path.dirname(db_abspath)
    try:
        subprocess.run(
            ["git", "-C", db_dir, "pull", "origin", "main"],
            check=True
        )
        print("git pull quiz läuft wie erwartet")
    except Exception as e:
        print("Git Pull im quiz Fehler:", e)

def git_push_db():
    """Führt einen Git Push für die Datenbank durch.
    Diese Funktion wird verwendet, um die aktuellen Änderungen in der Datenbank
    in das Git-Repository zu übertragen. Sie geht davon aus, dass die Datenbank
    in einem Git-Repository verwaltet wird.
    Vor dem Push wird die Datenbankdatei zum Commit hinzugefügt.
    """
    print("git push quiz läuft")
    db_abspath = os.path.abspath(DB_PATH)
    db_dir = os.path.dirname(db_abspath)
    db_file = os.path.basename(db_abspath)
    try:
        subprocess.run(["git", "-C", db_dir, "add", db_file], check=True)
        subprocess.run(["git", "-C", db_dir, "commit", "-m", "Update DB"], check=True)
        subprocess.run(["git", "-C", db_dir, "push", "origin", "main"], check=True)
        print("Hallo der Git Push quiz war erfolgreich.")
    except Exception as e:
        print("Git Push  quiz Fehler:", e)


        # fertig