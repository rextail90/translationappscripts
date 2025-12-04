# translators/deepl_api.py

import requests
from .base import BaseTranslator
from config import DEEPL_API_KEY, LANG_CODES

class DeepLTranslator(BaseTranslator):
    name = "DeepL"

    def __init__(self):
        if not DEEPL_API_KEY:
            raise ValueError("DEEPL_API_KEY is not set")
        self.endpoint = "https://api.deepl.com/v2/translate"

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        params = {
            "auth_key": DEEPL_API_KEY,
            "text": text,
            "source_lang": LANG_CODES.get(source_lang.lower(), source_lang),
            "target_lang": LANG_CODES.get(target_lang.lower(), target_lang),
        }
        resp = requests.post(self.endpoint, data=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data["translations"][0]["text"]
