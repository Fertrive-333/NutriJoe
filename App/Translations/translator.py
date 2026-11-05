import json
from pathlib import Path


class Translator:

    def __init__(self, language="es"):
        self.language = language
        self.translations = {}
        self.load_language(language)

    def load_language(self, language):

        path = (
            Path(__file__).resolve().parent
            / f"{language}.json"
        )

        with open(path, "r", encoding="utf-8") as file:
            self.translations = json.load(file)

        self.language = language

    def tr(self, key):
        return self.translations.get(key, key)