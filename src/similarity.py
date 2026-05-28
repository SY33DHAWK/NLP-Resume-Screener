import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from typing import Dict

# Load sentence transformer model once at module level
# so it doesn't reload on every function call
print("Loading sentence transformer model...")
SENTENCE_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
print("Model loaded.")


# ── Approach 1: TF-IDF Cosine Similarity ──────────────────────

def tfidf_similarity(resume_text: str, jd_text: str) -> float:
    """
    Compute cosine similarity between resume and JD
    using TF-IDF vectorization.
    Returns a score between 0.0 and 1.0
    """
    vectorizer = TfidfVectorizer()

    try:
        tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
        score = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
        return round(float(score), 4)
    except Exception:
        return 0.0


# ── Approach 2: Semantic Similarity ───────────────────────────

def semantic_similarity(resume_text: str, jd_text: str) -> float:
    """
    Compute semantic similarity using sentence transformers.
    Understands meaning, not just keyword overlap.
    Returns a score between 0.0 and 1.0
    """
    try:
        embeddings = SENTENCE_MODEL.encode(
            [resume_text[:512], jd_text[:512]]
        )
        score = cosine_similarity(
            [embeddings[0]], [embeddings[1]]
        )[0][0]
        return round(float(score), 4)
    except Exception:
        return 0.0


# ── Approach 3: Skill Overlap Score ───────────────────────────

def skill_overlap_score(
    resume_skills: list,
    jd_skills: list
) -> float:
    """
    Measure what percentage of JD skills
    are present in the resume.
    Returns a score between 0.0 and 1.0
    """
    if not jd_skills:
        return 0.0

    resume_set = set([s.lower() for s in resume_skills])
    jd_set = set([s.lower() for s in jd_skills])

    matched = resume_set.intersection(jd_set)
    score = len(matched) / len(jd_set)
    return round(score, 4)


# ── Combined Master Score ──────────────────────────────────────

def compute_match_score(
    resume_text: str,
    jd_text: str,
    resume_skills: list,
    jd_skills: list,
    weights: Dict[str, float] = None
) -> Dict:
    """
    Combines all three approaches into one
    final weighted match score.

    Default weights:
        TF-IDF similarity    → 25%
        Semantic similarity  → 50%
        Skill overlap        → 25%
    """
    if weights is None:
        weights = {
            "tfidf": 0.25,
            "semantic": 0.50,
            "skill_overlap": 0.25
        }

    # Compute individual scores
    tfidf_score   = tfidf_similarity(resume_text, jd_text)
    semantic_score = semantic_similarity(resume_text, jd_text)
    skill_score   = skill_overlap_score(resume_skills, jd_skills)

    # Weighted final score
    final_score = (
        tfidf_score   * weights["tfidf"] +
        semantic_score * weights["semantic"] +
        skill_score   * weights["skill_overlap"]
    )

    final_percentage = round(final_score * 100, 2)

    return {
        "tfidf_score":     round(tfidf_score * 100, 2),
        "semantic_score":  round(semantic_score * 100, 2),
        "skill_score":     round(skill_score * 100, 2),
        "final_score":     final_percentage,
        "match_label":     get_match_label(final_percentage)
    }


def get_match_label(score: float) -> str:
    """
    Convert numerical score into
    a human-readable match label.
    """
    if score >= 80:
        return "Excellent Match 🟢"
    elif score >= 60:
        return "Good Match 🟡"
    elif score >= 40:
        return "Partial Match 🟠"
    else:
        return "Low Match 🔴"