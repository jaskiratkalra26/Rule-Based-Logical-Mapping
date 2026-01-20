import re
import unicodedata

# Rule 1: Text must not be empty
def is_non_empty(text: str) -> bool:
    return len(text.strip()) > 0

# Rule 2: Text must contain N words
def has_minimum_words(text: str, n: int) -> bool:
    return len(text.split()) >= n

# Rule 3: If the input text is a question, identify which domain the question belongs to based on domain-specific keywords.
def detect_question_and_domain(text: str, domain_keywords: dict) -> dict:
    """
    Detects whether the input text is a question and identifies its domain.

    Returns:
        {
            "is_question": bool,
            "domain": str | None
        }
    """

    text_lower = text.lower()

    # Step 1: Question intent detection
    question_words = ["what", "how", "why", "when", "where", "which", "can", "does", "is"]
    is_question = (
        "?" in text_lower or
        any(text_lower.startswith(q + " ") for q in question_words)
    )

    if not is_question:
        return {
            "is_question": False,
            "domain": None
        }

    # Step 2: Domain detection
    # DOMAIN_KEYWORDS = {
#     "finance": ["refund", "payment", "pricing", "invoice"],
#     "account": ["login", "password", "account", "signup"],
#     "policy": ["policy", "terms", "conditions", "privacy"]
# }
    for domain, keywords in domain_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            return {
                "is_question": True,
                "domain": domain
            }

    # Step 3: Question detected but domain unknown
    return {
        "is_question": True,
        "domain": "unknown"
    }

# Rule 4: If the text exceeds the model’s token limit, use the model tokenizer to split the text into overlapping chunks aligned with token boundaries.
def chunk_text_with_tokenizer(
    text: str,
    tokenizer,
    max_tokens: int,
    overlap_tokens: int
) -> list[str]:
    """
    Splits text into chunks using a model tokenizer to respect
    actual token limits.
    """

    tokens = tokenizer.encode(text)
    chunks = []

    start = 0
    while start < len(tokens):
        end = start + max_tokens
        chunk_tokens = tokens[start:end]
        chunk_text = tokenizer.decode(chunk_tokens)
        chunks.append(chunk_text)

        start = end - overlap_tokens
        if start < 0:
            start = 0

    return chunks

# Rule 5: Remove or mask all offensive and abusive words from the input text before further NLP processing.
from better_profanity import profanity

def sanitize_offensive_language(text: str) -> str:
    profanity.load_censor_words()
    return profanity.censor(text)

# Rule 6: Detect and mask personally identifiable information (PII) such as email addresses and phone numbers using regular expressions before further NLP processing.


def mask_pii(text: str) -> str:
    """
    Masks common PII patterns such as emails and phone numbers
    using regular expressions.
    """

    # Email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'

    # Phone number pattern (10-digit, flexible separators)
    phone_pattern = r'\b(?:\+?\d{1,3}[\s-]?)?\d{10}\b'

    text = re.sub(email_pattern, '[EMAIL]', text)
    text = re.sub(phone_pattern, '[PHONE]', text)

    return text


# Rule 7: Normalize text by removing invisible Unicode characters, standardizing whitespace, and converting special characters into a consistent format before downstream NLP processing.

def normalize_text(text: str) -> str:
    """
    Normalizes unicode characters, whitespace, and invisible symbols
    to produce clean, consistent text for NLP pipelines.
    """

    # Unicode normalization (NFKC)
    text = unicodedata.normalize("NFKC", text)

    # Remove zero-width and invisible characters
    text = re.sub(r'[\u200B-\u200D\uFEFF]', '', text)

    # Normalize whitespace (tabs, newlines, multiple spaces)
    text = re.sub(r'\s+', ' ', text).strip()

    return text

# Rule 8: Split the input text into well-formed sentences using punctuation and normalize sentence boundaries before downstream NLP processing.


def split_into_sentences(text: str) -> list[str]:
    """
    Splits text into sentences using punctuation-based rules
    and normalizes sentence boundaries.
    """

    # Normalize whitespace first
    text = re.sub(r'\s+', ' ', text).strip()

    # Split on sentence-ending punctuation
    sentences = re.split(r'(?<=[.!?])\s+', text)

    # Remove very short or empty fragments
    sentences = [s.strip() for s in sentences if len(s.strip()) > 0]

    return sentences

# Rule 9: Remove URLs and web artifacts (links, tracking params) from the text before downstream NLP processing.


def remove_urls(text: str, replace_with: str = "") -> str:
    """
    Removes URLs from text using regex.
    """

    url_pattern = r'https?://\S+|www\.\S+'
    text = re.sub(url_pattern, replace_with, text)

    # Clean extra whitespace left behind
    text = re.sub(r'\s+', ' ', text).strip()

    return text

# Rule 10: Remove HTML and markup tags from the input text before downstream NLP processing.

def remove_html_tags(text: str) -> str:
    """
    Removes HTML and markup tags from text using regex.
    """

    html_tag_pattern = r'<[^>]+>'
    text = re.sub(html_tag_pattern, '', text)

    # Normalize whitespace after tag removal
    text = re.sub(r'\s+', ' ', text).strip()

    return text
