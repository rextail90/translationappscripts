# translators/google_ui.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .base import BaseTranslator
from .selenium_utils import create_driver


class GoogleUITranslator(BaseTranslator):
    name = "GoogleTranslateUI"

    def __init__(self, headless: bool = False):
        print("[Google] Initializing driver...")
        self.driver = create_driver(headless=headless)
        self.base_url = "https://translate.google.com/"

    def _find_input_box(self, d):
        ...
        textarea = WebDriverWait(d, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "textarea[aria-label][jsname]")
            )
        )
        return textarea

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        d = self.driver
        print("[Google] Navigating to page...")
        d.get(self.base_url)

        # (Optional) you can encode langs in URL if you want:
        # d.get(f"https://translate.google.com/?sl={source_lang}&tl={target_lang}&op=translate")

        src_box = self._find_input_box(d)
        print("[Google] Found input textarea")

        # Clear & type text
        src_box.clear()
        src_box.send_keys(text)

        print("[Google] Waiting for translation output...")
        out_elem = WebDriverWait(d, 30).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "#yDmH0d > c-wiz > div > div.ToWKne > c-wiz > div.OlSOob > c-wiz > div.ccvoYb > div.AxqVh > div.OPPzxe > c-wiz > div > div.usGWQd > div > div.lRu31 > span.HwtZe > span > span")
            )
        )

        result = out_elem.text.strip()
        print(f"[Google] Got translation: {result!r}")
        return result

    def close(self):
        print("[Google] Closing driver...")
        self.driver.quit()
