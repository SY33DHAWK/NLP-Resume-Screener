import re
import string
import nltk
import spacy

# Download required NLTK data on first run
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("punkt", quiet=True)

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize tools
lemmatizer = WordNetLemmatizer()
STOPWORDS = set(stopwords.words("english"))

# Skills we never want removed even if they look like stopwords
PRESERVE_TERMS = {
    "python", "r", "sql", "c", "c++", "java", "scala",
    "ml", "ai", "nlp", "llm", "api", "aws", "gcp", "etl",
}


def remove_urls(text: str) -> str:
    """Remove all URLs from text."""
    return re.sub(r"http\S+|www\S+|https\S+", " ", text)


def remove_emails(text: str) -> str:
    """Remove email addresses."""
    return re.sub(r"\S+@\S+", " ", text)


def remove_phone_numbers(text: str) -> str:
    """Remove phone numbers in various formats."""
    return re.sub(r"[\+\(]?[1-9][0-9\-\(\)\s]{8,}[0-9]", " ", text)


def remove_special_characters(text: str) -> str:
    """Remove special characters but keep spaces."""
    return re.sub(r"[^a-zA-Z0-9\s]", " ", text)


def remove_extra_whitespace(text: str) -> str:
    """Collapse multiple spaces and strip edges."""
    return re.sub(r"\s+", " ", text).strip()


def to_lowercase(text: str) -> str:
    """Convert all text to lowercase."""
    return text.lower()


def remove_stopwords(text: str) -> str:
    """
    Remove stopwords but preserve important
    technical terms defined in PRESERVE_TERMS.
    """
    words = text.split()
    filtered = [
        word for word in words
        if word not in STOPWORDS or word in PRESERVE_TERMS
    ]
    return " ".join(filtered)


def lemmatize_text(text: str) -> str:
    """Reduce words to their base form."""
    words = text.split()
    lemmatized = [lemmatizer.lemmatize(word) for word in words]
    return " ".join(lemmatized)


def clean_text(text: str, lemmatize: bool = True) -> str:
    """
    Master cleaning pipeline.
    Runs all steps in the correct order.
    """
    text = remove_urls(text)
    text = remove_emails(text)
    text = remove_phone_numbers(text)
    text = remove_special_characters(text)
    text = to_lowercase(text)
    text = remove_extra_whitespace(text)
    text = remove_stopwords(text)

    if lemmatize:
        text = lemmatize_text(text)

    text = remove_extra_whitespace(text)
    return text


def clean_for_display(text: str) -> str:
    """
    Lighter clean for displaying text in UI.
    Keeps structure readable, just removes noise.
    """
    text = remove_urls(text)
    text = remove_emails(text)
    text = remove_phone_numbers(text)
    text = remove_extra_whitespace(text)
    return text


def clean_resume(text: str) -> str:
    """Dedicated cleaner for resume text."""
    return clean_text(text, lemmatize=True)


def clean_job_description(text: str) -> str:
    """Dedicated cleaner for job description text."""
    return clean_text(text, lemmatize=True)