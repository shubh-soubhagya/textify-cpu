from python_scripts.ocr import extract_text, ocr
from python_scripts.spelling_corrections import correct_spelling
from python_scripts.spacings import add_space_after_punctuation
from spellchecker import SpellChecker
from python_scripts.groqllm import clean_text
import re


image_file = input("Image path: ")
text = extract_text(image_file)
corrected_text = correct_spelling(text)
final_text = add_space_after_punctuation(corrected_text)
corrected_text = final_text
textify_text= clean_text(corrected_text)
print(textify_text)  


