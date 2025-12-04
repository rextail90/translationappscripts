# run_csv_tests.py
#
# Loads test cases from data/test_cases.csv
# Runs them through all available translators
# Prints translations + BLEU + semantic similarity + error category

import pandas as pd
from typing import List

from translators.deepl_api import DeepLTranslator
from translators.google_api import GoogleTranslateAPITranslator
from translators.reverso_api import ReversoTranslator
from translators.itranslate_ui import ITranslateTranslator

from scoring import evaluate_translation
from error_analysis import classify_error


# ------------------------------------------------------------
# Build translators (skip gracefully if API keys missing)
# ------------------------------------------------------------

def build_translators():
    translators = []

    try:
        translators.append(DeepLTranslator())
        print("[INFO] DeepL loaded.")
    except Exception as e:
        print("[WARN] Skipping DeepL:", e)

    try:
        translators.append(GoogleTranslateAPITranslator())
        print("[INFO] Google Translate API loaded.")
    except Exception as e:
        print("[WARN] Skipping Google API:", e)

    try:
        translators.append(ReversoTranslator(headless=False))
        print("[INFO] Reverso loaded.")
    except Exception as e:
        print("[WARN] Skipping Reverso:", e)

    try:
        translators.append(ITranslateTranslator())
        print("[INFO] iTranslate loaded.")
    except Exception as e:
        print("[WARN] Skipping iTranslate:", e)

    return translators


# ------------------------------------------------------------
# Run CSV-driven tests
# ------------------------------------------------------------

def run_csv_tests():
    # Load your test_cases.csv
    df = pd.read_csv("data/test_cases.csv")

    translators = build_translators()

    print("\n================= RUNNING CSV TESTS =================\n")

    for _, row in df.iterrows():
        case_id = row["id"]
        domain = row.get("domain", "")
        src_lang = row["source_lang"]
        tgt_lang = row["target_lang"]
        src_text = row["source_text"]
        reference = row["reference_translation"]

        print(f"\n----- Test Case {case_id} ({domain}) -----")
        print(f"Source ({src_lang}): {src_text}")
        print(f"Reference: {reference}\n")

        for translator in translators:
            print(f"  >>> Translator: {translator.name}")

            try:
                translated = translator.translate(src_text, src_lang, tgt_lang)
            except Exception as e:
                print(f"    [ERROR] {translator.name} failed: {e}")
                translated = ""

            if translated:
                metrics = evaluate_translation(reference, translated)
                err_type = classify_error(reference, translated, metrics)

                print(f"    Output: {translated}")
                print(f"    BLEU: {metrics['bleu']:.3f}")
                print(f"    Semantic similarity: {metrics['semantic_similarity']:.3f}")
                print(f"    Tone score: {metrics['tone_score']:.3f}")
                print(f"    Error category: {err_type}")
            else:
                print("    No translation returned.")

        print("\n-------------------------------------------")

    # cleanup Selenium for UI translators
    for t in translators:
        close = getattr(t, "close", None)
        if callable(close):
            try:
                t.close()
            except Exception:
                pass
    
    print("\n================= DONE =================\n")


if __name__ == "__main__":
    run_csv_tests()
