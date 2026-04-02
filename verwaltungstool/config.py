from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # BASE_DIR findet den Projekt-Root von überall aus:
    # Pfad: config.py -> verwaltungstool -> Root

    def __init__(self):

        self.USER = None

        self.BASE_DIR = Path(__file__).resolve().parent.parent
        #Quiz
        self.QUIZ_DB = self.BASE_DIR / "verwaltungstool/data/sqlite/quiz_app.sqlite"
        self.QUIZ_JSON = self.BASE_DIR /  "verwaltungstool/data/json/quiz_scores.json"

        #Flashcards
        self.FLASHCARDS_DB = self.BASE_DIR / "verwaltungstool/data/sqlite/flashcards.sqlite"
        self.FLASHCARDS_JSON = self.BASE_DIR / "verwaltungstool/data/json/flashcards_scores.json"

        #Quotes
        self.QUOTES_DB = self.BASE_DIR / "verwaltungstool/data/sqlite/quotes.db"

        #StoerungenCounter
        self.COUNTER_DB = self.BASE_DIR / "verwaltungstool/data/sqlite/stoerungen.db"

        #News
        self.NEWS_DB = self.BASE_DIR / "verwaltungstool/data/sqlite/news.db"

        #Kalender
        self.CALENDAR_JSON = self.BASE_DIR / "verwaltungstool/data/json/meine_anwesenheit.json"

        #Aesthetik und Zierwerk
        self.ICON_DIR = self.BASE_DIR / "verwaltungstool/styles/images"

        # Lädt die .env immer aus dem Root-Verzeichnis
        load_dotenv(self.BASE_DIR / ".env")
        # Einstellungen
        self.SUPABASE_API_URL = "https://fburyyzzewkdqxutuayl.supabase.co"
        self.SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

        print("\n\n" + self.SUPABASE_API_KEY)

        # Pfade als Path-Objekte (Windows/Linux kompatibel)
        self.DATA_DIR = self.BASE_DIR / "data"
        self.LOG_DIR = self.BASE_DIR / "logs"
    # Zentrale Instanz bereitstellen

settings = Settings()