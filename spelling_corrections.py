from spellchecker import SpellChecker

def correct_spelling(text):
    """
    Corrects spelling errors in the text while preserving the original structure.
    """
    spell = SpellChecker()
    corrected_text = []

    # Split the text into lines to preserve line breaks
    lines = text.split("\n")

    for line in lines:
        corrected_line = []
        words = line.split()  # Split each line into words

        for word in words:
            # Correct the word if it's misspelled
            corrected_word = spell.correction(word)
            # Preserve the original word if the corrected word is None (e.g., for punctuation)
            corrected_line.append(corrected_word if corrected_word is not None else word)

        # Join the corrected words back into a line
        corrected_text.append(" ".join(corrected_line))

    # Join the lines back into a single text
    return "\n".join(corrected_text)