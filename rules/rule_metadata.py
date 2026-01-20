RULE_METADATA = [
    {
        "rule_id": "R1",
        "category": "validation",
        "rule_text": "Text must not be empty.",
        "function": "is_non_empty",
        "params": {},
        "description": "Validates that the input text contains at least one non-whitespace character."
    },
    {
    "rule_id": "R2",
    "category": "validation",
    "rule_text": "Text must contain N words.",
    "function": "has_minimum_words",
    "params": {"n": 3},
    "description": "Validates that the input text contains at least N words."
},
{
    "rule_id": "R3",
    "category": "intent_and_domain_routing",
    "rule_text": (
        "If the input text is a question, identify the domain "
        "of the question using domain-specific keywords."
    ),
    "function": "detect_question_and_domain",
    "params": {
        "domain_keywords": {
            "finance": ["refund", "payment", "pricing", "invoice"],
            "account": ["login", "password", "account", "signup"],
            "policy": ["policy", "terms", "conditions", "privacy"]
        }
    },
    "description": (
        "Detects question intent and routes the query to the "
        "appropriate domain for downstream AI or retrieval pipelines."
    )
},
{
    "rule_id": "R4",
    "category": "model_aware_chunking",
    "rule_text": (
        "If the text exceeds the model token limit, split it into "
        "overlapping chunks using the model tokenizer."
    ),
    "function": "chunk_text_with_tokenizer",
    "params": {
        "max_tokens": 512,
        "overlap_tokens": 50
    },
    "description": (
        "Ensures chunks respect model token limits and preserve "
        "semantic coherence for downstream embedding or LLM usage."
    )
},
{
    "rule_id": "R5",
    "category": "text_sanitization",
    "rule_text": (
        "Remove or mask all offensive and abusive words from the text "
        "before downstream NLP processing."
    ),
    "function": "sanitize_offensive_language",
    "params": {},
    "description": (
        "Uses a predefined profanity dictionary to sanitize offensive "
        "language and ensure safe AI pipeline execution."
    )
},
{
    "rule_id": "R6",
    "category": "pii_masking",
    "rule_text": (
        "Detect and mask personally identifiable information such as "
        "email addresses and phone numbers using regular expressions."
    ),
    "function": "mask_pii",
    "params": {},
    "description": (
        "Prevents exposure of sensitive personal information by masking "
        "PII before downstream NLP or AI processing."
    )
},
{
    "rule_id": "R7",
    "category": "text_normalization",
    "rule_text": (
        "Normalize text by removing invisible unicode characters "
        "and standardizing whitespace before NLP processing."
    ),
    "function": "normalize_text",
    "params": {},
    "description": (
        "Ensures consistent and clean text by normalizing unicode "
        "artifacts and whitespace, improving tokenizer and model stability."
    )
},
{
    "rule_id": "R8",
    "category": "sentence_normalization",
    "rule_text": (
        "Split input text into well-formed sentences using punctuation "
        "and normalize sentence boundaries."
    ),
    "function": "split_into_sentences",
    "params": {},
    "description": (
        "Ensures text is segmented into coherent sentences before "
        "chunking, embedding, or retrieval to preserve semantic meaning."
    )
},
{
    "rule_id": "R9",
    "category": "noise_removal",
    "rule_text": (
        "Remove URLs and web artifacts from text before downstream "
        "NLP processing."
    ),
    "function": "remove_urls",
    "params": {},
    "description": (
        "Eliminates non-linguistic URL noise to improve embedding quality "
        "and retrieval performance."
    )
},
{
    "rule_id": "R10",
    "category": "markup_cleanup",
    "rule_text": (
        "Remove HTML and markup tags from the text before "
        "downstream NLP processing."
    ),
    "function": "remove_html_tags",
    "params": {},
    "description": (
        "Strips HTML and markup artifacts to ensure clean, "
        "plain text input for NLP and AI pipelines."
    )
}
]