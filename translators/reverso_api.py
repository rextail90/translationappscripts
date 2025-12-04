# translators/reverso_api.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from .base import BaseTranslator
from .selenium_utils import create_driver


class ReversoTranslator(BaseTranslator):
    name = "ReversoContext"

    def __init__(self, headless: bool = False):
        print("[Reverso] Initializing driver...")
        self.driver = create_driver(headless=headless)
        self.base_url = "https://www.reverso.net/text-translation"

    def _find_input_box(self, d):
        print("[Reverso] Searching for contenteditable input...")

        # Look for ANY editable div (the one you showed in DevTools)
        elems = d.find_elements(By.CSS_SELECTOR, "div[contenteditable='true']")
        print(f"[Reverso] Found {len(elems)} contenteditable div(s)")

        if not elems:
            # As a fallback, also show how many textareas there are
            textareas = d.find_elements(By.TAG_NAME, "textarea")
            print(f"[Reverso] Fallback debug: found {len(textareas)} <textarea> elements")
            raise Exception("No contenteditable divs found on page")

        return elems[0]

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        d = self.driver
        print("[Reverso] Navigating to page...")
        d.get(self.base_url)

        # 1. Find the input box (contenteditable div)
        src_box = self._find_input_box(d)
        print("[Reverso] Found contenteditable input")

        # 2. Use JS to focus and set its text (no click / send_keys)
        print("[Reverso] Setting input text via JS...")
        d.execute_script("arguments[0].focus();", src_box)
        d.execute_script("arguments[0].innerHTML = '';", src_box)
        d.execute_script("arguments[0].innerText = arguments[1];", src_box, text)

        # 3. Fire input event so Reverso reacts
        d.execute_script(
            "arguments[0].dispatchEvent(new Event('input', {bubbles: true}));",
            src_box,
        )

        # 4. Wait for output translation span
        print("[Reverso] Waiting for translation output...")
        out_elem = WebDriverWait(d, 30).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "span.text__translation")
            )
        )

        result = out_elem.text.strip()
        print(f"[Reverso] Got translation: {result!r}")
        return result


    def close(self):
        print("[Reverso] Closing driver...")
        self.driver.quit()
