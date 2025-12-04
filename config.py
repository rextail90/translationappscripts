# config.py

import os
from dotenv import load_dotenv

load_dotenv()

# --- API KEYS (set via .env or environment) ---
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID", "")

# --- General settings ---
DATA_FILE = "data/test_cases.csv"           # your Deliverable 2B test cases
OUTPUT_LOG = "results/translation_results.csv"

# Language mapping (you can tweak)
LANG_CODES = {
    "arabic": "ar",
    "english": "en",
    "ar": "ar",
    "en": "en",
}

# Selenium options
SELENIUM_DRIVER_PATH = "drivers/chromedriver"   # adjust if needed
HEADLESS = True
