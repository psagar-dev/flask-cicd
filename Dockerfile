# Dockerfile
FROM python:3.12-slim

# Set working dir
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Flask’s default port
EXPOSE 5000

# Run with Gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]