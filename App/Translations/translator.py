# App/Core/translator.py
import json
from pathlib import Path

from PySide6.QtCore import QObject, Signal, QSettings


class Translator(QObject):
    language_changed = Signal()   # se emite al cambiar de idioma

    def __init__(self, language: str = "es"):
        super().__init__()
        self._translations: dict[str, str] = {}
        self.language = language
        self.set_language(language)

    def set_language(self, language: str) -> None:
        path = Path(__file__).resolve().parent / f"{language}.json"
        self._translations = json.loads(path.read_text(encoding="utf-8"))
        self.language = language
        QSettings("NutriJoe", "NutriJoe").setValue("language", language)
        self.language_changed.emit()

    def t(self, key: str) -> str:
        # Si falta la clave, devuelve la propia clave (así no rompe nada)
        return self._translations.get(key, key)