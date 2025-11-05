FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    postgresql-client \
    libpq-dev \
    python3-dev \
    build-essential \
    pkg-config \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Create user and home directory
RUN groupadd -r appuser && useradd -r -g appuser appuser
ENV HOME=/home/app/cafesiran
RUN mkdir -p $HOME && chown -R appuser:appuser $HOME
# Create static and media directories with proper permissions
RUN mkdir -p $HOME/static $HOME/media && chown -R appuser:appuser $HOME

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set working directory
WORKDIR $HOME

# Copy requirements first for better caching
COPY requirements.txt $HOME/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir

# Copy application code
COPY . $HOME/

# Collect static files as root (migrations will be handled at runtime)
RUN python manage.py collectstatic --no-input --clear || true

# Set ownership after operations
RUN chown -R appuser:appuser $HOME

# Switch to non-root user
USER appuser

CMD python manage.py migrate --no-input && \
    daphne -b 0.0.0.0 -p 8000 config.asgi:application