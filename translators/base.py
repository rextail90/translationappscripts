# translators/base.py

from abc import ABC, abstractmethod


class BaseTranslator(ABC):
    """
    Common interface for all translators.
    """

    # Human-readable name for logging/results
    name: str = "base"

    @abstractmethod
    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Translate `text` from `source_lang` to `target_lang`.
        Concrete translators must implement this.
        """
        raise NotImplementedError

    def close(self):
        """
        Optional cleanup hook (e.g., quit Selenium driver).
        Subclasses can override; by default it's a no-op.
        """
        pass


# Backwards-compat alias for any old code using `Translator`
Translator = BaseTranslator
