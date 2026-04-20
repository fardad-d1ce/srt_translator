# SRT translator app
# This app translates SRT files from English to Persian using the mT5 model.

# --- IMPORTS ---
import os
import logging
from pathlib import Path
import pysrt
from tqdm import tqdm
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# --- CONFIGURATION & LOGGING ---
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
INPUT_DIR = Path("SRT-input")
OUTPUT_DIR = Path("SRT-output")
MODEL_ID = "SeyedAli/English-to-Persian-Translation-mT5-V1"

# --- MODEL SETUP ---
logging.info("Initializing translation engine...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, legacy=False)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID)

def translate(text: str) -> str:
    """Translates a single string to Persian using the loaded mT5 model."""
    if not text.strip():
        return text
    inputs = tokenizer(text, return_tensors="pt").input_ids
    outputs = model.generate(inputs, max_new_tokens=150)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def process_srt_files():
    # Setup directories cleanly
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Get list of SRT files
    srt_files = list(INPUT_DIR.glob("*.srt"))
    
    if not srt_files:
        logging.warning(f"No SRT files found in {INPUT_DIR}")
        return

    logging.info(f"Found {len(srt_files)} files. Starting translation...")

    for srt_path in srt_files:
        output_path = OUTPUT_DIR / f"{srt_path.stem}_translated.srt"
        logging.info(f"Processing: {srt_path.name}")
        
        try:
            subs = pysrt.open(str(srt_path), encoding='utf-8')
            
            # Use tqdm progress bar for individual subtitle lines
            for sub in tqdm(subs, desc="Translating lines", leave=False):
                sub.text = translate(sub.text)
            
            # CRITICAL: Save ONCE per file, not once per line!
            subs.save(str(output_path), encoding='utf-8')
            logging.info(f"Done! Saved to {output_path}")
            
        except Exception as e:
            logging.error(f"Failed to process {srt_path.name}: {e}")

if __name__ == "__main__":
    process_srt_files()