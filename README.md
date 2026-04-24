![Static Badge](https://img.shields.io/badge/python-3.14-blue?logo=python&logoColor=%233776AB) ![Static Badge](https://img.shields.io/badge/Transformers-5.5.4-%23FFD21E?logo=huggingface&logoColor=%23FFD21E) ![Static Badge](https://img.shields.io/badge/PyTorch-2.11-%23EE4C2C?logo=PyTorch&logoColor=%23EE4C2C) ![Static Badge](https://img.shields.io/badge/Gradio-6.13.0-%23F97316?logo=Gradio&logoColor=%23F97316) ![Static Badge](https://img.shields.io/badge/Docker-4.70.0-%232496ED?logo=Docker&logoColor=%232496ED) (for Docker Devs)



# Subtitle `.srt` Translator
This project is a simple SRT file translator that uses the `mT5-base` model from HuggingFace.
-   User-friendly web-app GUI.
-   Multiple languages: [Language Support](#current-language-support).
-   Using new models from [HuggingFace](https://huggingface.co/models).
-   *Dockerized* image.

## Prerequisites
-   Python 3.14: [https://www.python.org/downloads/](https://www.python.org/downloads/)
-   [Docker Desktop](https://www.docker.com/) (for *Dockerized* image)

## Installation
⚠ If NOT familiar with **Git**, simply download the ZIP file.
1. Navigate to a desired directory.
    ```bash
    cd <YOUR_desired_directory>
    ```
2. Clone the repository by running:
    ```bash
    git clone https://github.com/d1ce/srt_translator.git
    cd srt_translator
    ```
## How to Use 
1.  
     - Install basic dependencies:
        ```bash
        pip install  -r requirements.txt
        ```
     - Install `PyTorch` (light version is enough):
        Example:
        ```bash
        # for windows without CUDA
        pip3 install torch
        ```
        ```bash
        # for linux without CUDA
        pip install torch --index-url https://download.pytorch.org/whl/cpu
        ```
        see [here](https://pytorch.org/get-started/locally/) to choose the compatible version with your system.

1. Run the web-app:
    ```bash
    python web_app.py
    ```
1. Open the web-app in your browser at `http://localhost:7860`.
1. Choose your intended translation from the list.
1. BAM! Download the output or look at `SRT-output` directory.
1. (optional) Clean up the `hf_cache` directory.
    ```bash
    rm -rf hf_cache
    ```
## *Dockerized* Image:
```bash
docker compose up --build
```
## How the Script Works
1. Reads the SRT files uploaded by the user.
2. Uses the `transformers` library to load a proper `mT5-base` model.
3. Downloads the model's weights from HuggingFace in `hf_cache` directory (~*500MB-1.5GB* download only ***ONCE***).
4. Generates translated SRT files into `SRT-output` directory.

## Roadmap
- [x] Add support for multiple languages ...
- [x] Add a user-friendly web-app GUI.
- [ ] Improve performance.
- [ ] Enhance GUI.

## Current Language Support

| From | To | Model |
| -- | -- | -- | 
English | French | "Helsinki-NLP/opus-mt_tiny_eng-fra"
| English | German | "Helsinki-NLP/opus-mt_tiny_eng-deu" |
| English | Persian | "SeyedAli/English-to-Persian-Translation-mT5-V1" |
| English | Spanish | "Helsinki-NLP/opus-mt_tiny_eng-spa" |
|||
| French | English | "Helsinki-NLP/opus-mt_tiny_fra-eng" |
|||
| Korean | English | "Helsinki-NLP/opus-mt_tiny_kor-eng" |

## Credits
-   [Helsinki-NLP](https://huggingface.co/Helsinki-NLP) for the models.
-   [SeyedAli](https://huggingface.co/SeyedAli) for the Persian model.
