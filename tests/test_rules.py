import unittest
import sys
import os
from unittest.mock import MagicMock

# Add the parent directory to sys.path to allow importing from rules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rules.rule_functions import (
    is_non_empty,
    has_minimum_words,
    detect_question_and_domain,
    chunk_text_with_tokenizer,
    sanitize_offensive_language,
    mask_pii,
    normalize_text,
    split_into_sentences,
    remove_urls,
    remove_html_tags
)

class TestRuleFunctions(unittest.TestCase):

    # Rule 1: Text must not be empty
    def test_is_non_empty(self):
        self.assertTrue(is_non_empty("Hello world"))
        self.assertFalse(is_non_empty(""))
        self.assertFalse(is_non_empty("   "))
        self.assertFalse(is_non_empty("\n\t"))
        self.assertTrue(is_non_empty("."))  # Punctuation only is still non-empty
        self.assertTrue(is_non_empty("   a   "))

    # Rule 2: Text must contain N words
    def test_has_minimum_words(self):
        self.assertTrue(has_minimum_words("one two three", 3))
        self.assertTrue(has_minimum_words("one two three four", 3))
        self.assertFalse(has_minimum_words("one two", 3))
        self.assertTrue(has_minimum_words("   one   two   three   ", 3))
        self.assertFalse(has_minimum_words("", 1))
        self.assertTrue(has_minimum_words("Word1. Word2.", 2)) # Punctuation attached often counts as word in simple split
        self.assertTrue(has_minimum_words("A B C D E", 5))

    # Rule 3: Detect question and domain
    def test_detect_question_and_domain(self):
        domain_keywords = {
            "finance": ["refund", "payment", "pricing", "invoice"],
            "account": ["login", "password", "account", "signup"],
            "policy": ["policy", "terms", "conditions", "privacy"]
        }

        # Not a question
        result = detect_question_and_domain("I want a refund.", domain_keywords)
        self.assertFalse(result["is_question"])
        self.assertIsNone(result["domain"])

        # Question with unknown domain
        result = detect_question_and_domain("What is the weather today?", domain_keywords)
        self.assertTrue(result["is_question"])
        self.assertEqual(result["domain"], "unknown")

        # Question with specific domain (finance)
        result = detect_question_and_domain("How do I get a refund?", domain_keywords)
        self.assertTrue(result["is_question"])
        self.assertEqual(result["domain"], "finance")
        
        # Question with specific domain (account) - using '?' detection
        result = detect_question_and_domain("password reset issue?", domain_keywords)
        self.assertTrue(result["is_question"])
        self.assertEqual(result["domain"], "account")

        # Case sensitivity check
        result = detect_question_and_domain("HOW DO I LOGIN?", domain_keywords)
        self.assertTrue(result["is_question"])
        self.assertEqual(result["domain"], "account")

        # Mixed domains (first match wins usually, depends on iteration order of dict or keywords)
        # "refund" (finance) and "account" (account)
        result = detect_question_and_domain("Can I get a refund to my account?", domain_keywords)
        self.assertTrue(result["is_question"])
        self.assertIn(result["domain"], ["finance", "account"])

    # Rule 4: Chunk text with tokenizer
    def test_chunk_text_with_tokenizer(self):
        # Mock tokenizer
        mock_tokenizer = MagicMock()
        # Simple mock: encode splits by space, decode joins by space
        mock_tokenizer.encode.side_effect = lambda x: x.split()
        mock_tokenizer.decode.side_effect = lambda x: " ".join(x)

        text = "word1 word2 word3 word4 word5 word6"
        max_tokens = 4
        overlap_tokens = 2

        chunks = chunk_text_with_tokenizer(text, mock_tokenizer, max_tokens, overlap_tokens)
        
        # Expected: 
        # 1. "word1 word2 word3 word4" (indices 0-4)
        # Next start = 4 - 2 = 2. 
        # 2. "word3 word4 word5 word6" (indices 2-6)
        # Next start = 6 - 2 = 4.
        # 3. "word5 word6" (indices 4-6)
        
        self.assertEqual(len(chunks), 3)
        self.assertEqual(chunks[0], "word1 word2 word3 word4")
        self.assertEqual(chunks[1], "word3 word4 word5 word6")
        self.assertEqual(chunks[2], "word5 word6")

        # Test case where text is shorter than max_tokens
        chunks_short = chunk_text_with_tokenizer("word1 word2", mock_tokenizer, 5, 2)
        self.assertEqual(len(chunks_short), 1)
        self.assertEqual(chunks_short[0], "word1 word2")

        # Test exact fit
        chunks_exact = chunk_text_with_tokenizer("a b c", mock_tokenizer, 3, 1)
        # 1. "a b c" (0-3). Next start = 3-1 = 2.
        # 2. "c" (2-3)
        self.assertEqual(len(chunks_exact), 2)
        self.assertEqual(chunks_exact[0], "a b c")
        self.assertEqual(chunks_exact[1], "c")

    # Rule 5: Sanitize offensive language
    def test_sanitize_offensive_language(self):
        # Note: better_profanity default list contains common profanities.
        # We assume 'shit' is in the default list.
        text = "This is shit."
        sanitized = sanitize_offensive_language(text)
        self.assertNotEqual(text, sanitized)
        self.assertIn("****", sanitized)
        
        clean_text = "This is clean."
        self.assertEqual(sanitize_offensive_language(clean_text), clean_text)
        
        # Case sensitivity (library dependent, usually insensitive)
        text_caps = "THIS IS SHIT"
        sanitized_caps = sanitize_offensive_language(text_caps)
        self.assertNotEqual(text_caps, sanitized_caps)

    # Rule 6: Mask PII
    def test_mask_pii(self):
        text = "Contact me at test@example.com or 1234567890."
        masked = mask_pii(text)
        self.assertIn("[EMAIL]", masked)
        self.assertIn("[PHONE]", masked)
        self.assertNotIn("test@example.com", masked)
        self.assertNotIn("1234567890", masked)

        text_no_pii = "Just some text."
        self.assertEqual(mask_pii(text_no_pii), text_no_pii)

        # Complex email
        text_complex = "user.name+tag@sub.example.co.uk"
        masked_complex = mask_pii(text_complex)
        self.assertEqual(masked_complex, "[EMAIL]")

        # Phone with country code (regex: \b(?:\+?\d{1,3}[\s-]?)?\d{10}\b)
        # Note: The regex starts with \b. Since '+' is not a word character, \b matches *after* the '+' 
        # (between + and the digit). So the '+' is left behind. This is expected behavior for this regex.
        text_phone_cc = "+1 1234567890" 
        masked_cc = mask_pii(text_phone_cc)
        self.assertEqual(masked_cc.strip(), "+[PHONE]")

    # Rule 7: Normalize text
    def test_normalize_text(self):
        # 1. NFKC normalization (e.g., ﬃ -> ffi)
        text_nfkc = "\ufb03ce" # ﬃce
        self.assertEqual(normalize_text(text_nfkc), "ffice")

        # 2. Invisible chars
        text_invisible = "Hello\u200BWorld"
        self.assertEqual(normalize_text(text_invisible), "HelloWorld")

        # 3. Whitespace
        text_spaces = "  Hello   World  \n "
        self.assertEqual(normalize_text(text_spaces), "Hello World")
        
        # Combined
        combined = "  \ufb03ce \u200B  "
        self.assertEqual(normalize_text(combined), "ffice")

        # Tabs
        text_tabs = "Col1\tCol2"
        self.assertEqual(normalize_text(text_tabs), "Col1 Col2")

    # Rule 8: Split into sentences
    def test_split_into_sentences(self):
        text = "Hello world. How are you? I am fine!"
        sentences = split_into_sentences(text)
        self.assertEqual(len(sentences), 3)
        self.assertEqual(sentences[0], "Hello world.")
        self.assertEqual(sentences[1], "How are you?")
        self.assertEqual(sentences[2], "I am fine!")

        text_weird_spacing = "Hello.    World."
        sentences_spacing = split_into_sentences(text_weird_spacing)
        self.assertEqual(sentences_spacing[0], "Hello.")
        self.assertEqual(sentences_spacing[1], "World.")
        
        # Abbreviations (known limitation of simple regex split: usually split)
        # We test that it DOES split, as the regex is simple.
        text_abbr = "Mr. Smith is here."
        sentences_abbr = split_into_sentences(text_abbr)
        self.assertEqual(len(sentences_abbr), 2) # Likely ["Mr.", "Smith is here."]
        self.assertEqual(sentences_abbr[0], "Mr.") 

    # Rule 9: Remove URLs
    def test_remove_urls(self):
        text = "Visit https://google.com for more info."
        cleaned = remove_urls(text)
        self.assertEqual(cleaned, "Visit for more info.")

        text_www = "Check www.example.com now."
        cleaned_www = remove_urls(text_www)
        self.assertEqual(cleaned_www, "Check now.")
        
        text_replacement = "Go to https://site.com"
        cleaned_repl = remove_urls(text_replacement, "[LINK]")
        self.assertEqual(cleaned_repl, "Go to [LINK]")

        # Multiple URLs
        text_multi = "http://a.com and https://b.com"
        self.assertEqual(remove_urls(text_multi), "and")

    # Rule 10: Remove HTML tags
    def test_remove_html_tags(self):
        text = "<div>Hello <b>World</b></div>"
        cleaned = remove_html_tags(text)
        self.assertEqual(cleaned, "Hello World")
        
        text_nested = "<p>Text <br> more text</p>"
        cleaned_nested = remove_html_tags(text_nested)
        self.assertEqual(cleaned_nested, "Text more text")

        # Attributes
        text_attr = '<a href="http://example.com" class="link">Link</a>'
        self.assertEqual(remove_html_tags(text_attr), "Link")

if __name__ == '__main__':
    unittest.main()
