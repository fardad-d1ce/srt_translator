import os
from pathlib import Path
import gradio as gr
import pysrt
from tqdm import tqdm
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, logging as transformers_logging

# --- CONFIGURATION ---
# INPUT_DIR = Path("SRT-input")
OUTPUT_DIR = Path("SRT-output")
CACHE_DIR = Path("hf_cache")
CACHE_DIR.mkdir(exist_ok=True)
transformers_logging.set_verbosity_error()

# Dictionary of supported languages and their models
SUPPORTED_TRANSLATIONS = {
    ("English", "French" ): "Helsinki-NLP/opus-mt_tiny_eng-fra",
    ("English", "German" ): "Helsinki-NLP/opus-mt_tiny_eng-deu",
    ("English", "Persian"): "SeyedAli/English-to-Persian-Translation-mT5-V1",
    ("English", "Spanish"): "Helsinki-NLP/opus-mt_tiny_eng-spa",
    ("French" , "English"): "Helsinki-NLP/opus-mt_tiny_fra-eng",
    ('Korean' , 'English'): "Helsinki-NLP/opus-mt_tiny_kor-eng"
}

SUPPORTED_SOURCE_LANGUAGES = list(set([key[0] for key in SUPPORTED_TRANSLATIONS.keys()]))
SUPPORTED_TARGET_LANGUAGES = list(set([key[1] for key in SUPPORTED_TRANSLATIONS.keys()]))


def translate_srt(files, source_lang, target_lang):
    logs = []
    translated_files = []
    
    def log_update(msg):
        logs.append(msg)
        return "\n".join(logs)

    try:
        model_id = SUPPORTED_TRANSLATIONS.get((source_lang, target_lang))
        if not model_id:
            yield None, log_update(f"❌ Translation from {source_lang} to {target_lang} is not supported.")
            return
            
        if not files:
            yield None, log_update("⚠️ Please upload at least one SRT file.")
            return

        yield None, log_update(f"🚀 Initializing translation: {source_lang} -> {target_lang}")
        yield None, log_update(f"📦 Loading model: {model_id}...")
        
        # --- MODEL SETUP ---
        tokenizer = AutoTokenizer.from_pretrained(model_id, legacy=False, cache_dir=str(CACHE_DIR))
        model = AutoModelForSeq2SeqLM.from_pretrained(model_id, cache_dir=str(CACHE_DIR))
        
        yield None, log_update("✅ Model loaded successfully!")
        OUTPUT_DIR.mkdir(exist_ok=True)

        for file_obj in files:
            srt_path = Path(file_obj.name)
            output_path = OUTPUT_DIR / f"{srt_path.stem}_{source_lang}_{target_lang}.srt"
            yield None, log_update(f"⏳ Processing: {srt_path.name}...")
            
            try:
                subs = pysrt.open(str(srt_path), encoding='utf-8')
                for sub in tqdm(subs, desc=f"Translating {srt_path.name}"):
                    if sub.text.strip():
                        inputs = tokenizer(sub.text, return_tensors="pt").input_ids
                        outputs = model.generate(inputs, max_new_tokens=150)
                        sub.text = tokenizer.decode(outputs[0], skip_special_tokens=True)
                
                subs.save(str(output_path), encoding='utf-8')
                translated_files.append(str(output_path))
                yield translated_files, log_update(f"✅ Finished: {srt_path.name} -> {output_path.name}")
            except Exception as e:
                error_msg = f"❌ Error processing {srt_path.name}: {str(e)}"
                yield translated_files, log_update(error_msg)
                print(error_msg)

        yield translated_files, log_update("✨ All tasks completed!")
        
    except Exception as e:
        yield translated_files, log_update(f"💥 Critical Error: {str(e)}")

# --- GRADIO INTERFACE ---
with gr.Blocks(title="SRT Translator 🎬") as demo:
    gr.Markdown("# SRT Translator 🎬")
    gr.Markdown("Upload your subtitle files (.srt) and select translation languages.")
    
    with gr.Row():
        file_input = gr.File(label="Upload SRT Files", file_count="multiple", file_types=[".srt"])
        source_lang_input = gr.Dropdown(choices=SUPPORTED_SOURCE_LANGUAGES, label="Source Language", value="English")
        target_lang_input = gr.Dropdown(choices=SUPPORTED_TARGET_LANGUAGES, label="Target Language", value="French")
    
    translate_btn = gr.Button("Translate Now", variant="primary")
    
    with gr.Row():
        file_output = gr.File(label="Download Translated Files")
        status_logs = gr.Textbox(label="Status Logs", interactive=False, lines=10)

    translate_btn.click(
        fn=translate_srt,
        inputs=[file_input, source_lang_input, target_lang_input],
        outputs=[file_output, status_logs]
    )

if __name__ == "__main__":
    demo.launch(share=False) # Set share=True if you want to give a temporary public link to someone!