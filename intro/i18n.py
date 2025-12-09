import os
from typing import Optional
from PySide6.QtGui import QPixmap 

DEFAULT_LOCALE = "de"

# Simple in-file translations. For more languages move these to JSON/YAML files under a locales/ folder.
_translations = {
    "de": {
        "intro.page_1_image": QPixmap(os.path.join("intro", "images", "img/intro_image_1.png")),
        "intro.page_1_text": "Willkommen zum Verwaltungstool!\n\nDieses Tool hilft Ihnen, verschiedene Verwaltungsaufgaben effizient zu erledigen.",
        "intro.page_2_image": QPixmap(os.path.join("intro", "images", "img/intro_image_2.png")),
        "intro.page_2_text": "Navigieren Sie durch die verschiedenen Module, um Funktionen wie Anwesenheitsverwaltung, Störungszähler und mehr zu nutzen.",
        "intro.next_button_text": "Weiter",
        "intro.back_button_text": "Zurück", 
    },
    "en": {
        "intro.page_1_image": QPixmap(os.path.join("intro", "images", "intro_image_1.png")),
        "intro.page_1_text": "Welcome to the Management Tool!\n\nThis tool helps you efficiently handle various management tasks.",
        "intro.page_2_image": QPixmap(os.path.join("intro", "images", "intro_image_2.png")),
        "intro.page_2_text": "Navigate through the different modules to utilize features like attendance management, fault counter, and more.",
        "intro.next_button_text": "Next",
        "intro.back_button_text": "Back",
    },
}

def get_pixmap(key: str, locale: Optional[str] = None) -> QPixmap:
    """Return localized QPixmap for key."""
    loc = locale or DEFAULT_LOCALE
    if image_path is None and loc != DEFAULT_LOCALE:
        image_path = _translations.get(loc, {}).get(key)
    if image_path:
        try:
            return QPixmap(image_path)
        except Exception:
            return None
    return None


def set_locale(locale: str) -> None:
    """Set default locale for subsequent calls (simple global setter)."""
    global DEFAULT_LOCALE
    if locale:
        DEFAULT_LOCALE = locale


def get_text(key: str, locale: Optional[str] = None, default: Optional[str] = None, **kwargs) -> str:
    """Return localized text for key. Replaces format placeholders using kwargs.

    Fallback order: requested locale -> DEFAULT_LOCALE -> return `default` or the key itself.
    """
    loc = locale or DEFAULT_LOCALE
    text = _translations.get(loc, {}).get(key)
    if text is None and loc != DEFAULT_LOCALE:
        text = _translations.get(DEFAULT_LOCALE, {}).get(key)
    if text is None:
        text = default if default is not None else key
    try:
        return text.format(**kwargs) if kwargs else text
    except Exception:
        return text


def add_translations(locale: str, mapping: dict) -> None:
    """Merge additional translations at runtime (optional helper)."""
    if locale not in _translations:
        _translations[locale] = {}
    _translations[locale].update(mapping)
# standartsprache deutscht 
# kann geändert werden 

CURRENT_LAGNUAGE = "de" # de / en

# datenstrucktur beispiel 
#Transslations = {
#    "de":  "willkomen",
#    "en": "wellcome"
#}