from spellchecker import SpellChecker


def spell_correction(text, language_code):
    # Map your custom language codes to the ones `SpellChecker` understands
    lang_map = {
        'English': 'en',
        'French': 'fr',
        'Deutsch': 'de',
        'Spanish': 'es'
    }
    language_code = lang_map.get(language_code, 'en')  # Default to English if not mapped

    spell = SpellChecker(language=language_code)
    original_words = text.split()
    misspelled = spell.unknown(original_words)
    for word in misspelled:
        corrected_word = spell.correction(word)
        text = text.replace(word, corrected_word)

    return text
