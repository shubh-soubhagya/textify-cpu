from ocr import model, tokenizer
from spelling_corrections import correct_spelling
from spacings import add_space_after_punctuation
from spellchecker import SpellChecker
from transformers import AutoModel, AutoTokenizer
import re

