![Static Badge](https://img.shields.io/badge/python-3.14-blue?logo=python&logoColor=%233776AB) ![Static Badge](https://img.shields.io/badge/Transformers-5.5.4-%23FFD21E?logo=huggingface&logoColor=%23FFD21E) ![Static Badge](https://img.shields.io/badge/PyTorch-2.11-%23EE4C2C?logo=PyTorch&logoColor=%23EE4C2C)
![Static Badge](https://img.shields.io/badge/Docker-4.70.0-%232496ED?logo=Docker&logoColor=%232496ED) (for Docker Dev)



# Subtitle `.srt` Translator
This project is a simple SRT file translator that uses the `mT5-base` model from HuggingFace.
-   Easy-to-use command-line interface.
-   English to French, Spanish, German, and Persian.
-   Dockerized image.

## Prerequisites
-   Python 3.14: [https://www.python.org/downloads/](https://www.python.org/downloads/).
-   Docker Desktop (optional): [https://www.docker.com/](https://www.docker.com/).

## Installation
⚠ If NOT familiar with **Git**, just download the ZIP file.
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
### Non-*Docker* users:
1. Put your SRT file(s) in the `SRT-input` directory.
2.  
     - Install basic dependencies:
        ```bash
        pip install  -r requirements.txt
        ```
     - Install `PyTorch`:
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
3. Run the `Python` script, *e.g.*:
    ```bash
    python srt_translator_app.py
    ```
4. Choose your intended translation from the list.
5. BAM! Check `SRT-output` directory.
6. (optional) Clean up the `hf_cache` directory.
    ```bash
    rm -rf hf_cache
    ```
### *Docker* setup:
```bash
docker compose up --build
```
## How the Script Works
1. Reads the SRT files from the `SRT-input` directory.
2. Uses the `transformers` library to load a proper `mT5-base` model.
3. Downloads the model's weights from HuggingFace in `hf_cache` directory (~*500MB-1.5GB* download only ***ONCE***).
4. Generates translated SRT files into `SRT-output` directory.

## Roadmap
- [x] Add support for multiple languages ...
- [ ] Add support for multiple models ...
- [ ] Add a user-friendly web-app GUI.
## Current Language Support
English to:
-   French
-   Spanish
-   German
-   Persian (Farsi)