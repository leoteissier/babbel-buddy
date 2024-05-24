import unittest
from src.spell_correction import spell_correction


class TestSpellCorrection(unittest.TestCase):

    def test_spell_correction_english(self):
        corrected_text = spell_correction("hello wrld", "English")
        self.assertEqual(corrected_text, "hello world")

    def test_spell_correction_french(self):
        corrected_text = spell_correction("bonjur le monde", "French")
        self.assertEqual(corrected_text, "bonjour le monde")

    def test_spell_correction_Spanish(self):
        corrected_text = spell_correction("Hola mund", "Spanish")
        self.assertEqual(corrected_text, "Hola mundo")

    def test_spell_correction_empty_input(self):
        original_text = ""
        corrected_text = spell_correction(original_text, 'english')
        self.assertEqual(corrected_text, "")

    def test_spell_correction_unsupported_language(self):
        original_text = "hello world"
        corrected_text = spell_correction(original_text, 'unsupported_language')
        self.assertEqual(corrected_text, original_text)


if __name__ == '__main__':
    unittest.main()
