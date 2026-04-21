![Static Badge](https://img.shields.io/badge/python-3.14-blue?logo=python&logoColor=%233776AB) ![Static Badge](https://img.shields.io/badge/Transformers-5.5.4-%23FFD21E?logo=huggingface&logoColor=%23FFD21E) ![Static Badge](https://img.shields.io/badge/PyTorch-2.11-%23EE4C2C?logo=PyTorch&logoColor=%23EE4C2C)
![Static Badge](https://img.shields.io/badge/Docker-4.70.0-%232496ED?logo=Docker&logoColor=%232496ED) (for Docker Dev)



# English-to-Persian SRT Translation Using mT5 Model - Ver 1.0

## Prerequisites
-   Python 3.14: [https://www.python.org/downloads/](https://www.python.org/downloads/).
-   Docker Desktop (optional): [https://www.docker.com/](https://www.docker.com/).
## How to Use
0. Navigate to a desired directory.
    ```bash
    cd <YOUR_desired_directory>
    ```
1. Clone the repository by running:
    ```bash
    git clone https://github.com/d1ce/srt_translator.git
    cd srt_translator
    ```
   ⚠ If NOT familiar with ***Git***, just download the ZIP file.

2. Put your SRT file(s) in the `SRT-input` directory.
3.   Non-***Docker*** users:
     - Install basic dependencies:
        ```bash
        pip install  -r requirements.txt
        ```
     - Install light CPU-based `PyTorch`:
        see [here](https://pytorch.org/get-started/locally/) to choose the compatible version with your system.
        Example:
        ```bash
        pip3 install torch # for windows
        ```
        ```bash
        pip install torch --index-url https://download.pytorch.org/whl/cpu # for linux
        ```
        ⚠ ***Docker*** users can, instead, run the Docker compose command:
        ```bash
        docker compose up --build
        ```
4. Run the `Python` script, *e.g.*:
    ```bash
    python srt_translator_app.py
    ```
5. Choose your intended translation from the list, and wait for translation.
6. Done!
    -   The translated SRTs will be in the `SRT-output` directory.
7. Clean up the `hf_cache` directory.
    ```bash
    rm -rf hf_cache
    ```

## How the Script Works
1. The script reads the SRT files from the `SRT-input` directory.
2. It uses the `transformers` library to load a proper `mT5-base` model.
3. The script downloads the model's weights from HuggingFace in `hf_cache` directory. (~*500MB-1.5GB*. Only downloaded ***ONCE***)
4. The script generate translated SRT files into `SRT-output` directory.

## Roadmap
- [x] Add support for multiple languages ...
- [ ] Add support for multiple models ...
- [ ] Add a user-friendly web-app GUI.
## Current Languages Supported
English to:
-   French
-   Spanish
-   German
-   Persian (Farsi)