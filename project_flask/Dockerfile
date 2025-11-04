# Use a slim official Python image
FROM python:3.11-slim

# Prevent Python from writing pyc files and enable stdout/stderr buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies required by some Python packages (psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port used by gunicorn
EXPOSE 8000

# Use gunicorn to serve the Flask app (module: project_flask.app -> app)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "project_flask.app:app", "--workers", "4"]
