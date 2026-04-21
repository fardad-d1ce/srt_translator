# SRT translator app
# This app translates SRT files from English to various languages.

# --- IMPORTS ---
import os
import logging
from pathlib import Path
from tqdm import tqdm

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, logging as transformers_logging
import pysrt

# --- CONFIGURATION & LOGGING ---
# 1. Standard logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
# 2. Transformers specific logging
transformers_logging.set_verbosity_error()
# 3. Aggressively silence the underlying HTTP library (urllib3)
logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)

# Project Directories
INPUT_DIR = Path("SRT-input")
OUTPUT_DIR = Path("SRT-output")

CACHE_DIR = Path("hf_cache") # Local folder for model weights ~1.5GB
CACHE_DIR.mkdir(exist_ok=True) # Ensure local cache directory exists
os.environ["HF_HOME"] = str(CACHE_DIR.absolute()) # Force Hugging Face to use this folder

# Dictionary of supported languages and their corresponding Hugging Face models
SOURCE_LANGUAGES = {
    1: "English"
}
TARGET_LANGUAGES = {
    1: "French",
    2: "Spanish",
    3: "German",
    4: "Persian"
}
TRANSLATION_MAP = {
    (1,4): "SeyedAli/English-to-Persian-Translation-mT5-V1",
    (1,1): "Helsinki-NLP/opus-mt-en-fr",
    (1,2): "Helsinki-NLP/opus-mt-en-es",
    (1,3): "Helsinki-NLP/opus-mt-en-de"
}

def select_language():
    print("\n--- SRT TRANSLATOR ---")
    print("Available source languages:")
    for key, lang in SOURCE_LANGUAGES.items():
        print(f"{key}. {lang}")
    print("Available target languages:")
    for key, lang in TARGET_LANGUAGES.items():
        print(f"{key}. {lang}")
    
    while True:
        source_choice = int(input("\nSelect source language (number): ").strip())
        target_choice = int(input("\nSelect target language (number): ").strip())
        if (source_choice, target_choice) in TRANSLATION_MAP:
            print(f"\nSelected source language: {SOURCE_LANGUAGES[source_choice]}")
            print(f"Selected target language: {TARGET_LANGUAGES[target_choice]}")
            print(f"Loading translation model: {TRANSLATION_MAP[(source_choice, target_choice)]}")
            print("Please Wait...\n")
            return (source_choice, target_choice), TRANSLATION_MAP[(source_choice, target_choice)]
        print("Translation not available for this combination.")

def translate(text: str, tokenizer, model) -> str:
    """Translates a single string to the target language."""
    if not text.strip():
        return text
    inputs = tokenizer(text, return_tensors="pt").input_ids
    outputs = model.generate(inputs, max_new_tokens=150)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def process_srt_files(translation_code, tokenizer, model):
    # Setup directories cleanly
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Get list of SRT files
    srt_files = list(INPUT_DIR.glob("*.srt"))
    
    if not srt_files:
        logging.warning(f"No SRT files found in {INPUT_DIR}")
        return

    logging.info(f"Found {len(srt_files)} files. Starting translation...")

    for srt_path in srt_files:
        output_path = OUTPUT_DIR / f"{srt_path.stem}_{SOURCE_LANGUAGES[translation_code[0]]}_to_{TARGET_LANGUAGES[translation_code[1]]}.srt"
        logging.info(f"Translating: {srt_path.name}")
        
        try:
            subs = pysrt.open(str(srt_path), encoding='utf-8')
            
            # Use tqdm progress bar for individual subtitle lines
            for sub in tqdm(subs, desc=f"Translating to {TARGET_LANGUAGES[translation_code[1]]}", leave=False):
                sub.text = translate(sub.text, tokenizer, model)
            
            # CRITICAL: Save ONCE per file, not once per line!
            subs.save(str(output_path), encoding='utf-8')
            logging.info(f"Done! Saved to {output_path}")
            
        except Exception as e:
            logging.error(f"Failed to process {srt_path.name}: {e}")

if __name__ == "__main__":
    (src_idx, tgt_idx), model_id = select_language()
    translation_code = (src_idx, tgt_idx)

    # --- MODEL SETUP ---
    logging.info(f"Initializing translation engine using {model_id}...")

    tokenizer = AutoTokenizer.from_pretrained(
        model_id, 
        legacy=False, 
        cache_dir=str(CACHE_DIR) # We pass cache_dir explicitly to override the system default
    )
    model = AutoModelForSeq2SeqLM.from_pretrained(
        model_id, 
        cache_dir=str(CACHE_DIR) # We pass cache_dir explicitly to override the system default
    )

    process_srt_files(translation_code, tokenizer, model)
