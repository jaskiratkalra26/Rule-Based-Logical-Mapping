#Valdidation rules

Rule 1: Text must not be empty.
Rule 2: Text must contain n words
Rule 3: If the input text is a question, identify which domain the question belongs to based on domain-specific keywords.

#Chunking
Rule 4: If the text exceeds the model’s token limit, use the model tokenizer to split the text into overlapping chunks aligned with token boundaries.

#Text Processing
Rule 5: Remove or mask all offensive and abusive words from the input text before further NLP processing.
Rule 6: Detect and mask personally identifiable information (PII) such as email addresses and phone numbers using regular expressions before further NLP processing.
Rule 7: Normalize text by removing invisible Unicode characters, standardizing whitespace, and converting special characters into a consistent format before downstream NLP processing.
Rule 8: Split the input text into well-formed sentences using punctuation and normalize sentence boundaries before downstream NLP processing.
Rule 9: Remove URLs and web artifacts (links, tracking params) from the text before downstream NLP processing.
Rule 10: Remove HTML and markup tags from the input text before downstream NLP processing.