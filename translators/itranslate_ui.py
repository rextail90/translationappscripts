# translators/itranslate_ui.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .base import BaseTranslator
from .selenium_utils import create_driver


class ITranslateUITranslator(BaseTranslator):
    name = "iTranslateUI"

    def __init__(self, headless: bool = False):
        print("[iTranslate] Initializing driver...")
        self.driver = create_driver(headless=headless)
        # use the web app URL that actually shows the translator UI
        self.base_url = "https://itranslate.com/translate/arabic-saudi-arabia-to-english-united-states"

    def _find_input_box(self, d):
        print("[iTranslate] Locating input box...")
        # Inspect the site and replace selector with the real one
        textarea = WebDriverWait(d, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "textarea[id='476b34ed764aae48599b930721f13436']")
            )
        )
        return textarea

    def _find_output_box(self, d):
        print("[iTranslate] Locating output box...")
        out_elem = WebDriverWait(d, 30).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "#translate-webapp > div > div.translateHolder > div.translateBox.target > div.targetText")
            )
        )
        return out_elem

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        d = self.driver
        print("[iTranslate] Navigating to page...")
        d.get(self.base_url)

        inp = src_box = self._find_input_box(d)
        src_box.clear()
        src_box.send_keys(text)

        inp.clear()
        inp.send_keys(text)

        out_elem = self._find_output_box(d)
        # after typing into input and locating out_elem
        WebDriverWait(d, 30).until(
            lambda drv: out_elem.text.strip() not in ("", text.strip())
        )

        result = out_elem.text.strip()
        print(f"[iTranslate] Got translation: {result!r}")
        return result

    def close(self):
        print("[iTranslate] Closing driver...")
        self.driver.quit()
