# Use a stable Python image (3.11 is a good balance between stability and features)
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Update CA certificates
RUN update-ca-certificates

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies with retry
RUN pip install --upgrade pip setuptools wheel && \
    pip install --retries 10 --timeout 60 -r requirements.txt

# Copy the rest of the application
COPY . .

# Train the model
RUN python pipeline/training_pipeline.py

# Expose the port
EXPOSE 5000

# Command to run the app
CMD ["python", "application.py"]