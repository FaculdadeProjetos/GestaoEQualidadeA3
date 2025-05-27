# Multi-stage build for better caching and smaller final image
FROM python:3.10-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Development stage
FROM base as development

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make wait script executable
RUN chmod +x wait-for-db.sh

EXPOSE 5000

# Use development server with hot reload
CMD ["./wait-for-db.sh", "flask", "run", "--host=0.0.0.0", "--debug"]

# Production stage
FROM base as production

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Make wait script executable
RUN chmod +x wait-for-db.sh

EXPOSE 5000

# Use production server
CMD ["./wait-for-db.sh", "gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"] 