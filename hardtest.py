# offline_eval.py
#
# Offline evaluation:
# - Uses data/test_cases.csv where outputs for each app are hardcoded
# - Computes metrics + error categories + PASS/FAIL

import pandas as pd
from scoring import evaluate_translation
from error_analysis import classify_error

APPS = ["deepl_output", "google_output", "reverso_output", "itranslate_output"]


# -------- PASS/FAIL RULE --------
def pass_fail(metrics, error_category):
    """
    Rule:
    PASS if semantic similarity >= 0.75 AND BLEU >= 0.40 AND no major error.
    FAIL otherwise.
    """

    if (
        metrics["semantic_similarity"] >= 0.75
        and metrics["bleu"] >= 0.40
        and error_category == "no_major_error"
    ):
        return "PASS"
    return "FAIL"


# -------- Main Evaluator --------
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
            app_name = app_col.replace("_output", "").capitalize()

            candidate = str(row.get(app_col, "")).strip()

            print(f"  >>> App: {app_name}")

            if not candidate:
                print("    No output provided.")
                continue

            # compute metrics
            metrics = evaluate_translation(ref, candidate)
            err_type = classify_error(ref, candidate, metrics)

            # PASS/FAIL determination
            verdict = pass_fail(metrics, err_type)

            print(f"    Output: {candidate}")
            print(f"    BLEU: {metrics['bleu']:.3f}")
            print(f"    Semantic similarity: {metrics['semantic_similarity']:.3f}")
            print(f"    Tone score: {metrics['tone_score']:.3f}")
            print(f"    Error category: {err_type}")
            print(f"    PASS/FAIL: {verdict}")

        print("\n------------------------------------------------------")

    print("\n================= DONE (OFFLINE EVAL) =================\n")


if __name__ == "__main__":
    run_offline_eval()

