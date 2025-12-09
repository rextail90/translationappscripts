# config.py

import os
from dotenv import load_dotenv

#from translators.google_api import GoogleUITranslator
#from translators.deepl_api import DeepLUITranslator
#from translators.itranslate_ui import ITranslateUITranslator
from translators.reverso_api import ReversoTranslator

load_dotenv()

# --- API KEYS (set via .env or environment) ---
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID", "")

# --- General settings ---
DATA_FILE = "data/test_cases.csv"           # your Deliverable 2B test cases
OUTPUT_LOG = "results/translation_results.csv"

ENABLED_TRANSLATORS = {
    #"google_ui": GoogleUITranslator,
    #"deepl_ui": DeepLUITranslator,
    #"itranslate_ui": ITranslateUITranslator,
    "reverso": ReversoTranslator,
}

# Language mapping (you can tweak)
LANG_CODES = {
    "arabic": "ar",
    "english": "en",
    "ar": "ar",
    "en": "en",
}

# Data & output locations
TEST_CASES_CSV = "data/test_cases.csv"
RESULTS_CSV = "data/results.csv"      # or one per system if you prefer
SOURCE_LANG_COLUMN = "source_lang"
TARGET_LANG_COLUMN = "target_lang"
TEXT_COLUMN = "source_text"
ID_COLUMN = "id"   # whatever your test_cases.csv uses as an identifier

# Selenium options
SELENIUM_DRIVER_PATH = "drivers/chromedriver"   # adjust if needed
HEADLESS = True
