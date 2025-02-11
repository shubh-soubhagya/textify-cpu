import re

def add_space_after_punctuation(text):
    # Regex to match punctuation marks and add a space after them
    corrected_text = re.sub(r'([.,!?;:])(?![ \n])', r'\1 ', text)
    return corrected_text