# ===============================
# Stage 1 — Base image
# ===============================
FROM python:3.10-slim AS base

# Set working directory
WORKDIR /app

# Prevent Python from buffering logs
ENV PYTHONUNBUFFERED=1

# ===============================
# Stage 2 — Install dependencies
# ===============================

# Install system dependencies (for numpy, sentence-transformers, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY app/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# ===============================
# Stage 3 — Copy source code
# ===============================
COPY app/ ./app
COPY data/ ./data
COPY config.yaml ./
COPY run.py ./

# Create necessary directories if not present
RUN mkdir -p data/embeddings data/raw data/processed

# ===============================
# Stage 4 — Expose and Run
# ===============================
EXPOSE 8000

# Default command to run FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
