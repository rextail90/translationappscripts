# offline_eval.py
#
# Offline evaluation:
# - Uses data/test_cases.csv where outputs for each app are hardcoded
# - No Selenium, no API calls
# - Just computes metrics + error categories for each app vs reference

import pandas as pd
from scoring import evaluate_translation
from error_analysis import classify_error

APPS = ["deepl_output", "google_output", "reverso_output", "itranslate_output"]

def run_offline_eval():
    df = pd.read_csv("data/test_cases.csv")

    print("\n================= OFFLINE EVAL (HARDCODED OUTPUTS) =================\n")

    for _, row in df.iterrows():
        case_id = row["id"]
        domain = row["domain"]
        src = row["source_text"]
        ref = row["reference_translation"]

        print(f"\n----- Test Case {case_id} ({domain}) -----")
        print(f"Source: {src}")
        print(f"Reference: {ref}\n")

        for app_col in APPS:
            app_name = app_col.replace("_output", "").capitalize()  # Deepl, Google, Reverso, Itranslate
            candidate = str(row.get(app_col, "")).strip()

            print(f"  >>> App: {app_name}")
            if not candidate:
                print("    No output provided.")
                continue

            metrics = evaluate_translation(ref, candidate)
            err_type = classify_error(ref, candidate, metrics)

            print(f"    Output: {candidate}")
            print(f"    BLEU: {metrics['bleu']:.3f}")
            print(f"    Semantic similarity: {metrics['semantic_similarity']:.3f}")
            print(f"    Tone score: {metrics['tone_score']:.3f}")
            print(f"    Error category: {err_type}")

        print("\n------------------------------------------------------")

    print("\n================= DONE (EVAL) =================\n")


if __name__ == "__main__":
    run_offline_eval()
