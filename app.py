from ocr import extract_text
from spelling_corrections import correct_spelling
from spacings import add_space_after_punctuation
from spellchecker import SpellChecker
from transformers import AutoModel, AutoTokenizer
from groqllm import clean_text
import torch

import re

torch_device = torch.device("cpu")

image_file = input("Image path: ")
# res = model.chat(tokenizer, image_file, ocr_type='ocr')
text = extract_text(image_file)
corrected_text = correct_spelling(text)
final_text = add_space_after_punctuation(corrected_text)
corrected_text = final_text
clean_text(corrected_text)
# print(chat_completion.choices[0].message.content)  


