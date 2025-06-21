# Use stable Python version
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && update-ca-certificates

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org \
    --retries 5 --timeout 100 -r requirements.txt

# Copy application code
COPY . .

# Install in development mode
RUN pip install -e .

# Train model
RUN python pipeline/training_pipeline.py

# Expose port
EXPOSE 5000

# Run application
CMD ["python", "application.py"]