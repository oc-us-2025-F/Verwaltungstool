import os
from typing import Optional

DEFAULT_LOCALE = "de"

# Simple in-file translations. For more languages move these to JSON/YAML files under a locales/ folder.
_translations = {
    "de": {
        "intro.title": "Willkommen",
        "intro.image_1.label": "Startbild: {owner}",
        "intro.image_2.label": "Zweite Folie",
        "intro.next": "Weiter",
        "intro.prev": "Zurück",
    },
    "en": {
        "intro.title": "Welcome",
        "intro.image_1.label": "Start image: {owner}",
        "intro.image_2.label": "Second slide",
        "intro.next": "Next",
        "intro.prev": "Previous",
    },
}


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