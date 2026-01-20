import unittest
import sys
import os
from unittest.mock import MagicMock

# Add the parent directory to sys.path to allow importing from rules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rules.rule_engine import RuleEngine

class TestRuleEngine(unittest.TestCase):

    def setUp(self):
        self.engine = RuleEngine()

    def test_apply_single_rule(self):
        # Test R1: Text must not be empty
        self.assertTrue(self.engine.apply_rule("R1", "Hello"))
        self.assertFalse(self.engine.apply_rule("R1", ""))

    def test_apply_rule_with_context(self):
        # Test R2: Text must contain N words (default N=3)
        self.assertTrue(self.engine.apply_rule("R2", "one two three"))
        
        # Override N in context
        self.assertTrue(self.engine.apply_rule("R2", "one two", context={"n": 2}))

    def test_process_pipeline_linear(self):
        # Pipeline: R7 (Normalize) -> R5 (Sanitize)
        # "\u200B badword " -> "badword" -> "****"
        
        text = "\u200B shit " 
        # R7 removes \u200B and trims -> "shit"
        # R5 sanitizes -> "****"
        
        result = self.engine.process_pipeline(text, ["R7", "R5"])
        self.assertEqual(result, "****")

    def test_process_pipeline_with_splitting(self):
        # Pipeline: R8 (Sentence Split) -> R5 (Sanitize)
        # "Hello shit. How are you?"
        # R8 -> ["Hello shit.", "How are you?"]
        # R5 mapped over list -> ["Hello ****.", "How are you?"]
        
        text = "Hello shit. How are you?"
        result = self.engine.process_pipeline(text, ["R8", "R5"])
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], "Hello ****.")
        self.assertEqual(result[1], "How are you?")

    def test_validate_all(self):
        text = "valid text here"
        results = self.engine.validate_all(text)
        # R1 and R2 are validation rules
        self.assertIn("R1", results)
        self.assertIn("R2", results)
        self.assertTrue(results["R1"])
        self.assertTrue(results["R2"])

    def test_invalid_rule_id(self):
        with self.assertRaises(ValueError):
            self.engine.apply_rule("INVALID_ID", "text")

if __name__ == '__main__':
    unittest.main()
