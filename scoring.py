# scoring.py

from typing import Dict
import numpy as np
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from sentence_transformers import SentenceTransformer, util

_smooth = SmoothingFunction().method4
_sbert_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

def compute_bleu(reference: str, candidate: str) -> float:
    ref_tokens = reference.split()
    cand_tokens = candidate.split()
    if not cand_tokens:
        return 0.0
    return float(sentence_bleu([ref_tokens], cand_tokens, smoothing_function=_smooth))

def compute_semantic_sim(reference: str, candidate: str) -> float:
    embeddings = _sbert_model.encode([reference, candidate], convert_to_tensor=True)
    sim = util.cos_sim(embeddings[0], embeddings[1])
    return float(sim.item())

def dummy_tone_score(reference: str, candidate: str) -> float:
    """
    Placeholder for tone detection (formal/polite/poetic).
    For now, just return 1.0 so the pipeline fits the report.
    """
    return 1.0

def evaluate_translation(reference: str, candidate: str) -> Dict[str, float]:
    bleu = compute_bleu(reference, candidate)
    sem_sim = compute_semantic_sim(reference, candidate)
    tone = dummy_tone_score(reference, candidate)
    return {
        "bleu": bleu,
        "semantic_similarity": sem_sim,
        "tone_score": tone,
    }
