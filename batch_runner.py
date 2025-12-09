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


def run_batch():
    # Make sure results directory exists
    os.makedirs(os.path.dirname(OUTPUT_LOG), exist_ok=True)

    # Load test cases once
    df = pd.read_csv(DATA_FILE)

    all_rows: List[Dict] = []

    # 🚀 Run ONE translator at a time
    for key, cls in ENABLED_TRANSLATORS.items():
        print(f"\n==============================")
        print(f"=== Running translator: {key} ===")
        print(f"==============================")

        try:
            translator = cls()
        except Exception as e:
            print(f"[WARN] Skipping translator {key}: {e}")
            continue

        try:
            for _, row in df.iterrows():
                case_id = row[ID_COLUMN]
                domain = row.get("domain", "")
                src_lang = row[SOURCE_LANG_COLUMN]
                tgt_lang = row[TARGET_LANG_COLUMN]
                src_text = row[TEXT_COLUMN]
                ref = row["reference_translation"]  # keep this name fixed in CSV

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

                all_rows.append(
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
        finally:
            # Always try to close this translator's driver
            close = getattr(translator, "close", None)
            if callable(close):
                close()

    out_df = pd.DataFrame(all_rows)

    # 1) Original results file (unchanged behavior)
    out_df.to_csv(OUTPUT_LOG, index=False)
    print(f"\nSaved results to {OUTPUT_LOG}")

    # 2) Add pass/fail and write a second CSV
    scored_df = out_df.copy()

    # PASS if no_major_error, FAIL otherwise (uses error_analysis.py)
    scored_df["pass_fail"] = scored_df["error_category"].apply(
        lambda c: "pass" if c == "no_major_error" else "fail"
    )

    scored_output = "results/translation_scored.csv"
    scored_df.to_csv(scored_output, index=False)
    print(f"Saved scored results to {scored_output}")



if __name__ == "__main__":
    run_batch()
