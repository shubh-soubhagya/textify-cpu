# from spellchecker import SpellChecker
from transformers import AutoModel, AutoTokenizer
# import re

tokenizer = AutoTokenizer.from_pretrained(
    'ucaslcl/GOT-OCR2_0', 
    trust_remote_code=True
)

model = AutoModel.from_pretrained(
    'ucaslcl/GOT-OCR2_0',
    trust_remote_code=True, 
    low_cpu_mem_usage=True, 
    device_map='cpu', 
    use_safetensors=True, 
    pad_token_id=tokenizer.eos_token_id
)

# Ensure model is on CPU
model = model.eval()
