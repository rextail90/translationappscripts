# translators/base.py

from abc import ABC, abstractmethod

class BaseTranslator(ABC):
    name: str

    @abstractmethod
    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate text from source_lang to target_lang."""
        raise NotImplementedError
