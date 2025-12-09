import time

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

        # NEW: open once and set language pair once
        self._open_page(self.driver)
        self._select_arabic_english(self.driver)

    # ---------- helpers copied from test_reverso.py (adapted) ----------

    def _open_page(self, d):
        print("[Reverso] Navigating to page...")
        d.get(self.base_url)
        time.sleep(3)

        # Close popup if present
        try:
            close_btn = d.find_element(
                By.CSS_SELECTOR,
                "button[aria-label*='close'], button[aria-label*='Close']",
            )
            if close_btn.is_displayed():
                close_btn.click()
                time.sleep(1)
        except Exception:
            pass

    def _select_arabic_english(self, d):
        """
        Reproduce the language-selection logic from test_reverso.py:
        left = Arabic, right = English.
        We ignore source_lang/target_lang parameters and assume ar→en.
        """

        # --- Left side: click current language, then choose Arabic ---
        print("[Reverso] Selecting Arabic as source language.")

        english_elements = d.find_elements(
            By.XPATH,
            "//*[contains(translate(text(), "
            "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'english')]",
        )

        for elem in english_elements:
            if (
                elem.is_displayed()
                and elem.location["x"] < 600
                and not elem.get_attribute("href")
                and elem.tag_name.lower() != "a"
            ):
                try:
                    wait = WebDriverWait(d, 5)
                    clickable_elem = wait.until(EC.element_to_be_clickable(elem))
                    clickable_elem.click()
                    time.sleep(2)
                    break
                except Exception:
                    elem.click()
                    time.sleep(2)
                    break

        time.sleep(1)

        arabic_options = d.find_elements(
            By.XPATH,
            "//*[contains(translate(text(), "
            "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'arabic')]",
        )

        arabic_selected = False
        for opt in arabic_options:
            if (
                opt.is_displayed()
                and not opt.get_attribute("href")
                and opt.tag_name.lower() in ["li", "button", "div", "span"]
            ):
                try:
                    wait = WebDriverWait(d, 5)
                    clickable_opt = wait.until(EC.element_to_be_clickable(opt))
                    clickable_opt.click()
                    time.sleep(1)
                    print("[Reverso] Selected Arabic (source)")
                    arabic_selected = True
                    break
                except Exception:
                    try:
                        opt.click()
                        time.sleep(1)
                        print("[Reverso] Selected Arabic (source, direct click)")
                        arabic_selected = True
                        break
                    except Exception:
                        continue

        if not arabic_selected:
            raise RuntimeError("Could not select Arabic as source language")

        # --- Right side: click current language (French), then choose English ---
        print("[Reverso] Selecting English as target language.")

        french_elements = d.find_elements(
            By.XPATH,
            "//*[contains(translate(text(), "
            "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'french')]",
        )

        french_button_y = None
        for elem in french_elements:
            if (
                elem.is_displayed()
                and elem.location["x"] > 300
                and not elem.get_attribute("href")
                and elem.tag_name.lower() != "a"
            ):
                french_button_y = elem.location["y"]
                try:
                    wait = WebDriverWait(d, 5)
                    clickable_elem = wait.until(EC.element_to_be_clickable(elem))
                    clickable_elem.click()
                    time.sleep(2)
                    break
                except Exception:
                    elem.click()
                    time.sleep(2)
                    break

        time.sleep(2)
        print("[Reverso] Looking for English in dropdown...")

        english_options = d.find_elements(
            By.XPATH,
            "//*[contains(translate(text(), "
            "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'english')]",
        )

        print(f"[Reverso] Found {len(english_options)} English elements")

        english_selected = False
        for opt in english_options:
            if not opt.is_displayed():
                continue
            if opt.tag_name.lower() == "a" or opt.get_attribute("href"):
                continue

            loc = opt.location
            tag_name = opt.tag_name.lower()

            is_in_dropdown = False
            if french_button_y:
                if loc["y"] > french_button_y + 20:
                    is_in_dropdown = True
            else:
                if 200 < loc["x"] < 800 and 300 < loc["y"] < 1000:
                    is_in_dropdown = True

            if not is_in_dropdown:
                continue

            if tag_name not in ["li", "button", "div", "span"]:
                continue

            text_lower = opt.text.strip().lower()
            if "english" in text_lower and len(text_lower) < 20:
                try:
                    wait = WebDriverWait(d, 5)
                    clickable_opt = wait.until(EC.element_to_be_clickable(opt))
                    clickable_opt.click()
                    time.sleep(2)
                    print(
                        f"[Reverso] Selected English (target) from {tag_name} at y={loc['y']}"
                    )
                    english_selected = True
                    break
                except Exception:
                    try:
                        opt.click()
                        time.sleep(2)
                        print(
                            f"[Reverso] Selected English (target, direct click) from {tag_name}"
                        )
                        english_selected = True
                        break
                    except Exception:
                        continue

        if not english_selected:
            raise RuntimeError("Could not select English as target language")

        time.sleep(2)

    def _find_input_box(self, d):
        print("[Reverso] Finding input box...")
        input_box = None

        # Prefer <textarea>
        try:
            textareas = d.find_elements(By.TAG_NAME, "textarea")
            for ta in textareas:
                if ta.is_displayed():
                    input_box = ta
                    break
        except Exception:
            pass

        # Fallback: left-side contenteditable div
        if not input_box:
            contenteditables = d.find_elements(
                By.CSS_SELECTOR, "div[contenteditable='true']"
            )
            for ce in contenteditables:
                if ce.is_displayed() and ce.location["x"] < 500:
                    input_box = ce
                    break

        if not input_box:
            raise RuntimeError("Could not find input box on Reverso page")

        print(f"[Reverso] Using {input_box.tag_name} as input box")
        return input_box

    def _enter_text(self, d, input_box, src_text: str):
        print(f"[Reverso] Entering text: {src_text!r}")
        time.sleep(2)

        try:
            wait = WebDriverWait(d, 5)
            clickable_input = wait.until(EC.element_to_be_clickable(input_box))
            clickable_input.click()
            time.sleep(0.3)
            try:
                clickable_input.clear()
            except Exception:
                pass
            clickable_input.send_keys(src_text)
            time.sleep(1)
            print("[Reverso] Text entered using Selenium")
        except Exception:
            print("[Reverso] Falling back to JavaScript to enter text")
            if input_box.tag_name.lower() == "textarea":
                d.execute_script(
                    "arguments[0].value = arguments[1];", input_box, src_text
                )
            else:
                d.execute_script(
                    "arguments[0].innerText = arguments[1];", input_box, src_text
                )
            d.execute_script(
                "arguments[0].dispatchEvent(new Event('input', {bubbles: true}));",
                input_box,
            )
            time.sleep(1)

    def _read_output(self, d, src_text: str) -> str:
        print("[Reverso] Waiting for translation...")
        time.sleep(5)

        src_clean = src_text.strip()

        # First: contenteditable on right side
        translation = None
        all_contenteditables = d.find_elements(By.CSS_SELECTOR, "div[contenteditable='true']")
        for elem in all_contenteditables:
            try:
                if not elem.is_displayed():
                    continue
                loc = elem.location
                txt = elem.text.strip()
                if (
                    loc["x"] > 400
                    and txt
                    and txt != src_clean
                    and len(txt) < 200
                    and "translate text" not in txt.lower()
                ):
                    translation = txt
                    break
            except StaleElementReferenceException:
                continue

        # Fallback: generic translation spans/divs
        if not translation:
            candidates = d.find_elements(
                By.CSS_SELECTOR,
                "div[class*='translation'], span[class*='translation']",
            )
            for elem in candidates:
                try:
                    if not elem.is_displayed():
                        continue
                    txt = elem.text.strip()
                    if (
                        txt
                        and txt != src_clean
                        and len(txt) < 200
                        and "translate text" not in txt.lower()
                    ):
                        translation = txt
                        break
                except StaleElementReferenceException:
                    continue

        if translation:
            # Try to extract the final English sentence from the blob
            lines = [l.strip() for l in translation.splitlines() if l.strip()]
            candidates = [
                l for l in lines
                if l != src_clean
                and "arabic" not in l.lower()
                and "english" not in l.lower()
                and "rephrase" not in l.lower()
                and "new" not in l.lower()
                and "/ 20000" not in l
            ]
            if candidates:
                translation = candidates[-1]

        if translation:
            print(f"[Reverso] Translation: {translation!r}")
        else:
            print("[Reverso] Could not reliably find translation text")

        return translation or ""


    # ---------- public API ----------

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        d = self.driver
        try:
            input_box = self._find_input_box(d)
            self._enter_text(d, input_box, text)
            return self._read_output(d, text)
        except Exception as e:
            print(f"[Reverso] ERROR during translate: {e}")
            return ""

    def close(self):
        print("[Reverso] Closing driver...")
        try:
            self.driver.quit()
        except Exception:
            pass
