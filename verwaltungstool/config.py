from pathlib import Path
import os
from dotenv import load_dotenv

class Settings:
    # BASE_DIR findet den Projekt-Root von überall aus:
    # Pfad: config.py -> verwaltungstool -> Root

    def __init__(self):
        self.BASE_DIR = Path(__file__).resolve().parent.parent

        self.QUIZ_DB = self.BASE_DIR / "verwaltungstool/data/sqlite/quiz_app.sqlite"
        self.QUIZ_JSON = self.BASE_DIR /  "verwaltungstool/data/json/quiz_scores.json"

        self.QUOTES_DB = self.BASE_DIR / "verwaltungstool/data/sqlite/quotes.db"

        self.COUNTER_DB = self.BASE_DIR / "verwaltungstool/data/sqlite/stoerungen.db"

        self.NEWS_DB = self.BASE_DIR / "verwaltungstool/data/sqlite/news.db"

        self.CALENDAR_JSON = self.BASE_DIR / "verwaltungstool/data/json/meine_anwesenheit.json"

        self.ICON_DIR = self.BASE_DIR / "verwaltungstool/styles/images"

        # Lädt die .env immer aus dem Root-Verzeichnis
        load_dotenv(self.BASE_DIR / ".env")
        # Einstellungen
        self.DB_URL = os.getenv("SUPABASE_URL")
        self.DB_KEY = os.getenv("SUPABASE_KEY")
        # Pfade als Path-Objekte (Windows/Linux kompatibel)
        self.DATA_DIR = self.BASE_DIR / "data"
        self.LOG_DIR = self.BASE_DIR / "logs"
    # Zentrale Instanz bereitstellen

settings = Settings()