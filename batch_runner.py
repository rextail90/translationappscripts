# batch_runner.py

import os
from typing import List, Dict

import pandas as pd

from config import (
    DATA_FILE,
    OUTPUT_LOG,
    SOURCE_LANG_COLUMN,
    TARGET_LANG_COLUMN,
    TEXT_COLUMN,
    ID_COLUMN,
    ENABLED_TRANSLATORS,
)
from scoring import evaluate_translation
from error_analysis import classify_error


def build_translators():
    """Instantiate all enabled translators from config.ENABLED_TRANSLATORS."""
    translators = []
    for key, cls in ENABLED_TRANSLATORS.items():
        try:
            t = cls()
            translators.append(t)
        except Exception as e:
            print(f"[WARN] Skipping translator {key}: {e}")
    return translators


def run_batch():
    # Make sure results directory exists
    os.makedirs(os.path.dirname(OUTPUT_LOG), exist_ok=True)

    # Load test cases
    df = pd.read_csv(DATA_FILE)

    translators = build_translators()
    rows: List[Dict] = []

    for _, row in df.iterrows():
        case_id = row[ID_COLUMN]
        domain = row.get("domain", "")
        src_lang = row[SOURCE_LANG_COLUMN]
        tgt_lang = row[TARGET_LANG_COLUMN]
        src_text = row[TEXT_COLUMN]
        ref = row["reference_translation"]  # keep this name fixed in CSV

        for translator in translators:
            try:
                translated = translator.translate(src_text, src_lang, tgt_lang)
            except Exception as e:
                print(f"[ERROR] {translator.name} failed on case {case_id}: {e}")
                translated = ""

            if translated:
                metrics = evaluate_translation(ref, translated)
            else:
                metrics = {
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
