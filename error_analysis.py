# error_analysis.py

from typing import Dict

def classify_error(reference: str, candidate: str, metrics: Dict[str, float]) -> str:
    bleu = metrics["bleu"]
    sim = metrics["semantic_similarity"]

    # thresholds are arbitrary; you can tune or just explain them in the report
    if sim > 0.85 and bleu > 0.5:
        return "no_major_error"
    if sim < 0.4:
        return "literal_mistranslation"
    if 0.4 <= sim < 0.7 and bleu < 0.3:
        return "lost_cultural_meaning"
    if 0.7 <= sim < 0.85 and bleu < 0.3:
        return "tone_mismatch"
    # You can add domain/dialect heuristics here if you tag your rows
    return "other"

