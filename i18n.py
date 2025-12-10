import os
from typing import Optional
# QPixmap wird HIER NICHT MEHR BENÖTIGT und wurde entfernt.

DEFAULT_LOCALE = "de" # verwendete sprache möglich: "de" / "en"

# Simple in-file translations. 
_translations = {
    "de": {
        # ✅ Speichert jetzt NUR DEN PFAD-STRING.
        "intro.page_1.image": os.path.join("intro", "images", "img/intro_image_1.png"),
        "intro.page_1.text": "Willkommen zum Verwaltungstool!\n\nDieses Tool hilft Ihnen, verschiedene Verwaltungsaufgaben effizient zu erledigen.",
        "intro.page_2.image": os.path.join("intro", "images", "img/intro_image_2.png"),
        "intro.page_2.text": "Navigieren Sie durch die verschiedenen Module, um Funktionen wie Anwesenheitsverwaltung, Störungszähler und mehr zu nutzen.",
        "intro.next_button_text": "Weiter",
        "intro.back_button_text": "Zurück", 
    },
    "en": {
        "intro.page_1.image": os.path.join("intro", "images", "intro_image_1.png"),
        "intro.page_1.text": "Welcome to the Management Tool!\n\nThis tool helps you efficiently handle various management tasks.",
        "intro.page_2.image": os.path.join("intro", "images", "intro_image_2.png"),
        "intro.page_2.text": "Navigate through the different modules to utilize features like attendance management, fault counter, and more.",
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