import os
from typing import Optional
# QPixmap wird HIER NICHT MEHR BENÖTIGT und wurde entfernt.

DEFAULT_LOCALE = "de" # verwendete sprache möglich: "de" / "en"

# Simple in-file translations. 
_translations = {
    "de": {
        # ✅ Speichert jetzt NUR DEN PFAD-STRING.
        "intro.page_1.image": os.path.join("intro", "images", "img/dashboard.png"),
        "intro.page_1.text": "Willkommen zum Verwaltungstool!\n\nDieses Multitool hilft Ihnen, ihre Umschulungsverwaltung effizient zu erledigen. Navigieren Sie durch die verschiedenen Module, um Funktionen wie Anwesenheitsverwaltung, Störungszähler und mehr zu nutzen",
        "intro.page_2.image": os.path.join("intro", "images", "img/anwesenheitskalender_1.png"),
        "intro.page_2.text": "Im Anwesenheitskalender verwalten Sie ihre Zeiten in einer kompakten Übersicht.",
        "intro.page_3.image": os.path.join("intro", "images", "img/anwesenheitskalender_2.png"),
        "intro.page_3.text": "Ihnen stehe jegliche Optionen frei, ihre Anwesenheit zu hinterlegen.",
        "intro.page_4.image": os.path.join("intro", "images", "img/anwesenheitskalender_3.png"),
        "intro.page_4.text": "Erhalten Sie eine Übersicht über vergangene Tage und zukünftige Planung.",
        "intro.page_5.image": os.path.join("intro", "images", "img/fragen.png"),
        "intro.page_5.text": "Stellen Sie Fragen an die Community!",
        "intro.page_6.image": os.path.join("intro", "images", "img/quiz.png"),
        "intro.page_6.text": "Erstellen Sie Inhalte für das Community-Quiz für eine bessere Prüfungsvorbereitung.",
        "intro.page_7.image": os.path.join("intro", "images", "img/stoerungscounter.png"),
        "intro.page_7.text": "IT = Problemlösung - Hier eine Möglichkeit alle Störungen die Sie während der Umschulung haben aufzuzählen.",
        "intro.page_8.image": os.path.join("intro", "images", "img/passwort_generierung.png"),
        "intro.page_8.text": "Brauchen Sie ein Passwort? - Kein Problem! Hier können Sie ein sicheres Passwort erstellen.",
        "intro.next_button_text": "Weiter",
        "intro.back_button_text": "Zurück", 
    },
    "en": { #TODO: Nixon Englische Übersetzung / alle XXXXXXXXXXXX kommentare abändern.
        "intro.page_1.image": os.path.join("intro", "images", "img/dashboard.png"),
        "intro.page_1.text": "xxxxxxxxxxxxxxxxx.",
        "intro.page_2.image": os.path.join("intro", "images", "img/anwesenheitskalender_1.png"),
        "intro.page_2.text": "xxxxxxxxxxxxxxxx.",
        "intro.page_3.image": os.path.join("intro", "images", "img/anwesenheitskalender_2.png"),
        "intro.page_3.text": "xxxxxxxxxxxxxxxx.",
        "intro.page_4.image": os.path.join("intro", "images", "img/anwesenheitskalender_3.png"),
        "intro.page_4.text": "xxxxxxxxxxxxxxxx.",
        "intro.page_5.image": os.path.join("intro", "images", "img/fragen.png"),
        "intro.page_5.text": "xxxxxxxxxxxxxxxx!",
        "intro.page_6.image": os.path.join("intro", "images", "img/quiz.png"),
        "intro.page_6.text": "xxxxxxxxxxxxxxxx.",
        "intro.page_7.image": os.path.join("intro", "images", "img/stoerungscounter.png"),
        "intro.page_7.text": "xxxxxxxxxxxxxxxx.",
        "intro.page_8.image": os.path.join("intro", "images", "img/passwort_generierung.png"),
        "intro.page_8.text": "xxxxxxxxxxxxxxxx.",

        "intro.next_button_text": "Next",
        "intro.back_button_text": "Back",
    },
}

def set_locale(locale: str) -> None:
    """Set default locale for subsequent calls (simple global setter)."""
    global DEFAULT_LOCALE
    if locale:
        DEFAULT_LOCALE = locale

# Hauptübersetzungsfunktion, umbenannt von get_text zu t,
# da sie in IntroManager als i18n.t verwendet wird.
def t(key: str, locale: Optional[str] = None, default: Optional[str] = None, **kwargs) -> str:
    """Gibt lokalisierten Text ODER den Bildpfad für den Key zurück."""
    loc = locale or DEFAULT_LOCALE
    
    # 1. Im angeforderten Locale suchen
    result = _translations.get(loc, {}).get(key)
    
    # 2. Fallback zum Standard-Locale
    if result is None and loc != DEFAULT_LOCALE:
        result = _translations.get(DEFAULT_LOCALE, {}).get(key)
    
    # 3. Fallback zum Default-Wert oder Key
    if result is None:
        result = default if default is not None else key
    
    # String-Formatierung anwenden (falls kwargs übergeben wurden)
    try:
        return result.format(**kwargs) if kwargs and isinstance(result, str) else result
    except Exception:
        return result


def add_translations(locale: str, mapping: dict) -> None:
    """Merge additional translations at runtime (optional helper)."""
    if locale not in _translations:
        _translations[locale] = {}
    _translations[locale].update(mapping)

# standartsprache deutscht 
# kann geändert werden 

CURRENT_LAGNUAGE = "de" # de / en