from spellchecker import SpellChecker


def spell_correction(text, language_code):
    """
    Correct the spelling of the given text based on the specified language code.

    :param text: The text to be corrected.
    :param language_code: The language code to determine the language for spell checking.
    :return: The text with corrected spelling.
    """
    # Map custom language codes to the ones `SpellChecker` understands
    lang_map = {
        'English': 'en',
        'French': 'fr',
        'Deutsch': 'de',
        'Spanish': 'es'
    }
    # Default to English if the provided language code is not in the map
    language_code = lang_map.get(language_code, 'en')

    # Initialize the SpellChecker with the specified language
    spell = SpellChecker(language=language_code)
    # Split the text into individual words
    original_words = text.split()
    # Identify the misspelled words
    misspelled = spell.unknown(original_words)

    # Iterate through each misspelled word and correct it
    for word in misspelled:
        corrected_word = spell.correction(word)
        # Replace the misspelled word in the text with the corrected word
        text = text.replace(word, corrected_word)

    # Return the text with corrected spelling
    return text