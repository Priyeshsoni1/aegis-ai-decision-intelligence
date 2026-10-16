
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    HF_HOME=/home/app/.cache/huggingface

WORKDIR /app

COPY . .

# Install CPU-only PyTorch to avoid downloading CUDA libraries.
RUN python -m pip install --no-cache-dir \
    --index-url https://download.pytorch.org/whl/cpu \
    --extra-index-url https://pypi.org/simple \
    "torch==2.7.1+cpu"

# Install Aegis and its remaining dependencies.
RUN python -m pip install --no-cache-dir .

# Run as a non-root user.
RUN useradd --create-home --shell /usr/sbin/nologin appuser \
    && mkdir -p /app/data /home/app/.cache/huggingface \
    && chown -R appuser:appuser /app/data /home/app/.cache

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
