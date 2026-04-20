# English-to-Persian SRT Translation Using mT5 Model
V1.0

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
3.   Non-***Docker*** users can install the dependencies:
        ```bash
        pip install -r requirements.txt
        ```

- ***Docker*** users can instead run the Docker compose command:
    ```bash
    docker compose up --build
    ```
4. Run the script:
    ```bash
    python translator.py
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