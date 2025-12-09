from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

from .base import BaseTranslator
from .selenium_utils import create_driver


class ReversoTranslator(BaseTranslator):
    name = "ReversoContext"

    def __init__(self, headless: bool = False):
        print("[Reverso] Initializing driver...")
        self.driver = create_driver(headless=headless)
        self.base_url = "https://www.reverso.net/text-translation"

    # ---------- helpers ----------

    def _find_input_box(self, d):
        """
        Use the big textarea on the left as input.
        """
        print("[Reverso] Searching for input box...")
        # Prefer the left textarea
        textareas = d.find_elements(By.TAG_NAME, "textarea")
        for ta in textareas:
            if ta.is_displayed() and ta.location.get("x", 0) < 500:
                print("[Reverso] Using left-side <textarea> as input")
                return ta

        # Fallback: look for a contenteditable div on the left
        content_divs = d.find_elements(By.CSS_SELECTOR, "div[contenteditable='true']")
        for div in content_divs:
            if div.is_displayed() and div.location.get("x", 0) < 500:
                print("[Reverso] Using left-side contenteditable div as input")
                return div

        raise Exception("No suitable input box found on Reverso page")

    def _get_output_text(self, d, src_text: str) -> str:
        """
        Wait until we can read some non-empty translation text
        from the right-hand side. We return the TEXT, not the element,
        so we don't suffer from stale element references.
        """
        print("[Reverso] Locating output text...")

        def _search(driver):
            # Look for the main translation spans Reverso uses
            candidates = driver.find_elements(
                By.CSS_SELECTOR,
                "div.context-result span.transliteration.transliteration_rtl, "
                "div.context-result span.transliteration"
            )
            best_text = None
            best_len = 0
            src_clean = src_text.strip()

            for el in candidates:
                try:
                    if not el.is_displayed():
                        continue
                    txt = el.text.strip()
                    if not txt:
                        continue
                    if txt == src_clean:
                        continue
                    if len(txt) > best_len:
                        best_text = txt
                        best_len = len(txt)
                except StaleElementReferenceException:
                    # Element disappeared while scanning – just skip it
                    continue
                except Exception:
                    continue

            return best_text  # WebDriverWait treats None as "keep waiting"

        # Wait until _search returns a non-None, non-empty string
        return WebDriverWait(d, 30).until(lambda drv: _search(drv))

    # ---------- main API ----------

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        d = self.driver
        print("[Reverso] Navigating to page...")
        d.get(self.base_url)

        src_box = self._find_input_box(d)
        print("[Reverso] Found visible left-side input")

        # Clear previous content
        try:
            src_box.clear()
        except Exception:
            # some contenteditable divs don’t support clear()
            d.execute_script("arguments[0].innerHTML = '';", src_box)

        src_box.send_keys(text)

        # Get the translation text directly (no element handles outside the wait)
        translated_text = self._get_output_text(d, text)
        print(f"[Reverso] Got translation: {translated_text!r}")
        return translated_text

    def close(self):
        print("[Reverso] Closing driver...")
        self.driver.quit()

