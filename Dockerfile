# Hugging Face Spaces runs this on a free CPU Space (Docker SDK), serving on port 7860.
FROM python:3.11-slim

# libglib2.0-0 is needed by opencv-python-headless at runtime.
RUN apt-get update \
    && apt-get install -y --no-install-recommends libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install deps first so they cache across code changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Reduce TensorFlow log noise.
ENV TF_CPP_MIN_LOG_LEVEL=2

EXPOSE 7860

# --timeout 120 gives the first (cold) prediction time to load TensorFlow.
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "--workers", "1", "--timeout", "120", "app:app"]
