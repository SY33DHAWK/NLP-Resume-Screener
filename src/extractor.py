import spacy
import re
from typing import Dict, List

nlp = spacy.load("en_core_web_sm")

# ── Master Skills Library ──────────────────────────────────────
SKILLS_DB = {
    "programming_languages": [
        "python", "r", "sql", "java", "scala", "c++", "c#",
        "javascript", "typescript", "bash", "matlab", "julia"
    ],
    "data_science": [
        "machine learning", "deep learning", "nlp",
        "natural language processing", "computer vision",
        "statistical analysis", "data mining", "feature engineering",
        "exploratory data analysis", "eda", "time series",
        "regression", "classification", "clustering",
        "reinforcement learning", "transfer learning"
    ],
    "ml_frameworks": [
        "scikit-learn", "tensorflow", "pytorch", "keras",
        "xgboost", "lightgbm", "catboost", "hugging face",
        "transformers", "spacy", "nltk", "gensim",
        "sentence-transformers", "openai"
    ],
    "data_tools": [
        "pandas", "numpy", "matplotlib", "seaborn", "plotly",
        "tableau", "power bi", "excel", "jupyter", "dbt",
        "apache spark", "hadoop", "airflow", "kafka"
    ],
    "databases": [
        "mysql", "postgresql", "mongodb", "sqlite", "redis",
        "snowflake", "bigquery", "oracle", "elasticsearch"
    ],
    "cloud_devops": [
        "aws", "gcp", "azure", "docker", "kubernetes",
        "ci/cd", "git", "github", "mlflow", "fastapi",
        "flask", "streamlit", "rest api", "microservices"
    ],
    "soft_skills": [
        "communication", "teamwork", "leadership", "problem solving",
        "critical thinking", "time management", "collaboration",
        "adaptability", "project management", "agile", "scrum"
    ]
}

# ── Degree Keywords ────────────────────────────────────────────
EDUCATION_KEYWORDS = [
    "bachelor", "master", "phd", "doctorate", "bsc", "msc",
    "b.sc", "m.sc", "b.tech", "m.tech", "mba", "computer science",
    "data science", "statistics", "mathematics", "engineering",
    "information technology"
]

# ── Experience Patterns ────────────────────────────────────────
EXPERIENCE_PATTERNS = [
    r"(\d+)\+?\s*years?\s*of\s*experience",
    r"(\d+)\+?\s*years?\s*experience",
    r"experience\s*of\s*(\d+)\+?\s*years?",
    r"over\s*(\d+)\s*years?",
]

# ── Job Title Keywords ─────────────────────────────────────────
JOB_TITLES = [
    "data scientist", "data analyst", "ml engineer",
    "machine learning engineer", "nlp engineer", "ai engineer",
    "data engineer", "business analyst", "software engineer",
    "backend developer", "frontend developer", "full stack developer",
    "devops engineer", "research scientist", "product manager"
]


def extract_skills(text: str) -> Dict[str, List[str]]:
    """
    Match text against skills DB.
    Returns found skills grouped by category.
    """
    text_lower = text.lower()
    found_skills = {}

    for category, skills in SKILLS_DB.items():
        matched = [
            skill for skill in skills
            if skill in text_lower
        ]
        if matched:
            found_skills[category] = matched

    return found_skills


def extract_all_skills_flat(text: str) -> List[str]:
    """
    Returns a flat list of all matched skills.
    Useful for similarity comparison.
    """
    found = extract_skills(text)
    flat = []
    for skills in found.values():
        flat.extend(skills)
    return list(set(flat))


def extract_education(text: str) -> List[str]:
    """Extract education level and field from text."""
    text_lower = text.lower()
    found = [
        keyword for keyword in EDUCATION_KEYWORDS
        if keyword in text_lower
    ]
    return list(set(found))


def extract_experience_years(text: str) -> int:
    """
    Extract years of experience mentioned in text.
    Returns the highest number found, or 0 if none.
    """
    text_lower = text.lower()
    years_found = []

    for pattern in EXPERIENCE_PATTERNS:
        matches = re.findall(pattern, text_lower)
        for match in matches:
            years_found.append(int(match))

    return max(years_found) if years_found else 0


def extract_job_titles(text: str) -> List[str]:
    """Extract mentioned job titles from text."""
    text_lower = text.lower()
    found = [
        title for title in JOB_TITLES
        if title in text_lower
    ]
    return found


def extract_named_entities(text: str) -> Dict[str, List[str]]:
    """
    Use spaCy NER to extract organizations,
    locations, and dates from text.
    """
    doc = nlp(text[:10000])  # spaCy limit safeguard
    entities = {
        "organizations": [],
        "locations": [],
        "dates": []
    }

    for ent in doc.ents:
        if ent.label_ == "ORG":
            entities["organizations"].append(ent.text)
        elif ent.label_ == "GPE":
            entities["locations"].append(ent.text)
        elif ent.label_ == "DATE":
            entities["dates"].append(ent.text)

    # Deduplicate
    for key in entities:
        entities[key] = list(set(entities[key]))

    return entities


def extract_all(text: str) -> Dict:
    """
    Master extractor — runs all extractors
    and returns one unified profile dict.
    """
    return {
        "skills": extract_skills(text),
        "all_skills_flat": extract_all_skills_flat(text),
        "education": extract_education(text),
        "experience_years": extract_experience_years(text),
        "job_titles": extract_job_titles(text),
        "entities": extract_named_entities(text)
    }