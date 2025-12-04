# translators/itranslate_ui.py

import time
from .base import BaseTranslator
from .selenium_utils import create_driver
from selenium.webdriver.common.by import By

class ITranslateTranslator(BaseTranslator):
    name = "iTranslate"

    def __init__(self):
        self.driver = create_driver()
        self.base_url = "https://www.itranslate.com/translation"  # adjust if needed

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        d = self.driver
        d.get(self.base_url)
        time.sleep(2)

        # Again, selectors are placeholders; inspect the page and adjust.
        src_box = d.find_element(By.CSS_SELECTOR, "textarea.source-textarea")
        src_box.clear()
        src_box.send_keys(text)

        # TODO: select languages via dropdowns if needed

        time.sleep(3)
        out_elem = d.find_element(By.CSS_SELECTOR, "div.target-text")
        return out_elem.text.strip()

    def close(self):
        self.driver.quit()
