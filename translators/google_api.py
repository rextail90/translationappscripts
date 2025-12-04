# translators/google_api.py

import requests
from .base import BaseTranslator
from config import GOOGLE_API_KEY, GOOGLE_PROJECT_ID, LANG_CODES

class GoogleTranslateAPITranslator(BaseTranslator):
    name = "GoogleTranslateAPI"

    def __init__(self):
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is not set")
        self.endpoint = (
            "https://translation.googleapis.com/language/translate/v2"
        )

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        params = {
            "key": GOOGLE_API_KEY,
            "q": text,
            "source": LANG_CODES.get(source_lang.lower(), source_lang),
            "target": LANG_CODES.get(target_lang.lower(), target_lang),
            "format": "text",
        }
        resp = requests.post(self.endpoint, data=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data["data"]["translations"][0]["translatedText"]
