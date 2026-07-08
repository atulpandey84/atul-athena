# Use official Python runtime as a parent image
FROM python:3.12-slim as builder

# Set work directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.12-slim

WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy source and documentation
COPY src/ /app/src/
COPY docs/ /app/docs/
COPY scripts/ /app/scripts/
COPY mkdocs.yml /app/

# Set environment variables
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

# Expose API port
EXPOSE 8000

# Default health check
HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1

# Start the API
CMD ["uvicorn", "athena.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
