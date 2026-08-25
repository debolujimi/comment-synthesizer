import importlib
import unittest


class TestCommentsGeneration(unittest.TestCase):
    def test_translate_chat_module_exists(self):
        module = importlib.import_module("comments_generation_wordnet_rulebased")
        self.assertTrue(hasattr(module, "translate_chat"))

    def test_translate_chat_for_loadshedding(self):
        module = importlib.import_module("comments_generation_wordnet_rulebased")
        response = module.translate_chat("there is loadshedding again")
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)

    def test_specific_phrase_beats_generic_word(self):
        module = importlib.import_module("comments_generation_wordnet_rulebased")
        response = module.translate_chat("there is a power outage in my area")
        self.assertIn("outage", response.lower())
        self.assertNotIn("severe pressure", response.lower())

    def test_hyphenated_loadshedding_variant(self):
        module = importlib.import_module("comments_generation_wordnet_rulebased")
        response = module.translate_chat("load-shedding started again")
        self.assertIn("loadshedding", response.lower())

    def test_misspelled_and_concatenated_variants(self):
        module = importlib.import_module("comments_generation_wordnet_rulebased")
        responses = [
            module.translate_chat("loadshedding started again"),
            module.translate_chat("there is a powercut in my area"),
            module.translate_chat("no electricity again"),
        ]
        for response in responses:
            self.assertIsInstance(response, str)
            self.assertTrue(len(response) > 0)
            self.assertNotEqual(response, "Unrecognized Message")

    def test_unknown_message_has_helpful_fallback(self):
        module = importlib.import_module("comments_generation_wordnet_rulebased")
        response = module.translate_chat("this is a weird message without any real topic")
        self.assertIn("loadshedding", response.lower())
        self.assertIn("outages", response.lower())

    def test_confidence_prefers_specific_outage_message(self):
        module = importlib.import_module("comments_generation_wordnet_rulebased")
        response = module.translate_chat("there is a power outage in my area")
        self.assertIn("outage", response.lower())

    def test_loadshedding_stage_variants(self):
        module = importlib.import_module("comments_generation_wordnet_rulebased")
        response = module.translate_chat("eskom stage 2 again")
        self.assertIn("loadshedding", response.lower())


if __name__ == "__main__":
    unittest.main()
