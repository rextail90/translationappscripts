# batch_runner.py

import os
from typing import List, Dict

import pandas as pd

from config import DATA_FILE, OUTPUT_LOG
from translators.deepl_api import DeepLTranslator
from translators.google_api import GoogleTranslateAPITranslator
from translators.reverso_api import ReversoTranslator
from translators.itranslate_ui import ITranslateTranslator
from scoring import evaluate_translation
from error_analysis import classify_error

def build_translators():
    translators = []
    # If an API key is missing, you can skip that translator
    try:
        translators.append(DeepLTranslator())
    except Exception as e:
        print("Skipping DeepL:", e)

    try:
        translators.append(GoogleTranslateAPITranslator())
    except Exception as e:
        print("Skipping Google Translate API:", e)

    # UI-based
    try:
        translators.append(ReversoTranslator())
    except Exception as e:
        print("Skipping Reverso:", e)

    try:
        translators.append(ITranslateTranslator())
    except Exception as e:
        print("Skipping iTranslate:", e)

    return translators

def run_batch():
    os.makedirs(os.path.dirname(OUTPUT_LOG), exist_ok=True)
    df = pd.read_csv(DATA_FILE)

    translators = build_translators()
    rows: List[Dict] = []

    for _, row in df.iterrows():
        case_id = row["id"]
        domain = row.get("domain", "")
        src_lang = row["source_lang"]
        tgt_lang = row["target_lang"]
        src_text = row["source_text"]
        ref = row["reference_translation"]

        for translator in translators:
            try:
                translated = translator.translate(src_text, src_lang, tgt_lang)
            except Exception as e:
                print(f"[ERROR] {translator.name} failed on case {case_id}: {e}")
                translated = ""
            
            metrics = evaluate_translation(ref, translated) if translated else {
                "bleu": 0.0,
                "semantic_similarity": 0.0,
                "tone_score": 0.0,
            }
            err_type = classify_error(ref, translated, metrics)

            rows.append(
                {
                    "case_id": case_id,
                    "domain": domain,
                    "translator": translator.name,
                    "source_lang": src_lang,
                    "target_lang": tgt_lang,
                    "source_text": src_text,
                    "reference_translation": ref,
                    "translated_text": translated,
                    "bleu": metrics["bleu"],
                    "semantic_similarity": metrics["semantic_similarity"],
                    "tone_score": metrics["tone_score"],
                    "error_category": err_type,
                }
            )

    # Cleanup UI drivers
    for t in translators:
        close = getattr(t, "close", None)
        if callable(close):
            close()

    out_df = pd.DataFrame(rows)
    out_df.to_csv(OUTPUT_LOG, index=False)
    print(f"Saved results to {OUTPUT_LOG}")

if __name__ == "__main__":
    run_batch()
