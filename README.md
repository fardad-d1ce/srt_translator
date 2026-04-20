![Static Badge](https://img.shields.io/badge/python-3.14-blue?logo=python&logoColor=%233776AB) ![Static Badge](https://img.shields.io/badge/Transformers-5.5.4-%23FFD21E?logo=huggingface&logoColor=%23FFD21E) ![Static Badge](https://img.shields.io/badge/PyTorch-2.11-%23EE4C2C?logo=PyTorch&logoColor=%23EE4C2C)
![Static Badge](https://img.shields.io/badge/Docker-4.70.0-%232496ED?logo=Docker&logoColor=%232496ED) (for Docker Dev)



# English-to-Persian SRT Translation Using mT5 Model - Ver 1.0

## Prerequisites
-   Python 3.14: [https://www.python.org/downloads/](https://www.python.org/downloads/).
-   Docker Desktop (optional): [https://www.docker.com/](https://www.docker.com/).
## Installation
1. Clone the repository by running:
    ```bash
    git clone https://github.com/d1ce/srt_translator.git
    cd srt_translator
    ```
   ⚠ If NOT familiar with ***Git***, just download the ZIP file.

2. Put your SRT file(s) in the `SRT-input` directory.
3.   Non-***Docker*** users;
     - Install basic dependencies:
        ```bash
        pip install  -r basic_requirements.txt
        ```
     - Install `PyTorch`: see [here](https://pytorch.org/get-started/locally/) to choose the compatible version with your system.
        For Windows users without CUDA:
        ```bash
        pip3 install torch torchvision
        ```

        ⚠ ***Docker*** users can, instead, run the Docker compose command:
        ```bash
        docker compose up --build
        ```
4. Run the `Python` script, *e.g.*:
    ```bash
    python srt_translator_app.py
    ```
5. Done!
    -   The translated SRTs will be in the `SRT-output` directory.

## How the Script Works
1. The script reads the SRT files from the `SRT-input` directory.
2. It uses the `transformers` library to load a proper [`mT5-base` model](https://huggingface.co/SeyedAli/English-to-Persian-Translation-mT5-V1).
3. The script downloads the model's weights from HuggingFace.
(~*1.5GB*. Only done once per session)
4. The script using the model, the translated SRT files is saved back to `SRT-output` directory.

## Roadmap
- [ ] Add support for multiple languages.
- [ ] Add support for multiple models.