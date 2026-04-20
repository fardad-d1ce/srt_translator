FROM python:3.14-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && rm -rf /var/lib/apt/lists/*

RUN useradd -m appuser
WORKDIR /home/appuser

# Install standard stuff
RUN pip install --no-cache-dir \
    jupyterlab \
    transformers \
    sentencepiece \
    protobuf \
    pysrt tqdm
# Install the "Engine" (Torch)
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

USER appuser