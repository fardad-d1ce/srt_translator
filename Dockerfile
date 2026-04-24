# Use the latest stable Python 3.14 slim
FROM python:3.14-slim

# Install system dependencies (needed for compiling some C-based tokenizers)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user for security and file management
RUN useradd -m appuser
WORKDIR /home/appuser

# Install standard packages first
RUN pip install --no-cache-dir \
    jupyterlab \
    transformers \
    pysrt \
    sacremoses \
    tqdm \
    sentencepiece \
    gradio

# Install CPU-only PyTorch (Save ~2GB compared to the full version)
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Ensure the appuser owns their home directory
RUN chown -R appuser:appuser /home/appuser

USER appuser

# Standard Jupyter port
EXPOSE 8888

# Start JupyterLab by default
ENV JUPYTER_TOKEN="hey"
CMD ["sh", "-c", "jupyter lab --ip=0.0.0.0 --no-browser --allow-root"]
