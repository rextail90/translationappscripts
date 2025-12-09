# translators/deepl_ui.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .base import BaseTranslator
from .selenium_utils import create_driver


class DeepLUITranslator(BaseTranslator):
    name = "DeepLUI"

    OUTPUT_SELECTOR = "span[class*='container-target']"

    def __init__(self, headless: bool = False):
        print("[DeepL] Initializing driver...")
        self.driver = create_driver(headless=headless)
        self.base_url = "https://www.deepl.com/translator"

    def _find_input_box(self, d):
        print("[DeepL] Locating source input (textarea or contenteditable)...")
        elem = WebDriverWait(d, 20).until(
            EC.presence_of_element_located(
                # first matching element: <textarea> OR editable div
                (By.CSS_SELECTOR, "textarea, div[contenteditable='true']")
            )
        )
        return elem

    def _find_output_box(self, d):
        print("[DeepL] Locating target text element...")
        out_elem = WebDriverWait(d, 30).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, self.OUTPUT_SELECTOR)
            )
        )
        return out_elem


    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        d = self.driver
        print("[DeepL] Navigating to page...")
        d.get(self.base_url)

        src_box = self._find_input_box(d)
        print("[DeepL] Found source textarea/contenteditable")

        # Type the text
        src_box.clear()
        src_box.send_keys(text)

        out_box = self._find_output_box(d)

        # Wait until DeepL actually fills in the translation text
        print("[DeepL] Waiting for output text...")
        WebDriverWait(d, 30).until(
            lambda drv: out_box.text.strip() != ""
        )

        result = out_box.text.strip()
        print(f"[DeepL] Got translation: {result!r}")
        return result

    def close(self):
        print("[DeepL] Closing driver...")
        self.driver.quit()