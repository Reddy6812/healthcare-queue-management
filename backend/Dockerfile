# Use official Python runtime.
FROM python:3.9-slim

# Set working directory.
WORKDIR /app

# Install system dependencies.
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Copy requirements and install them.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project.
COPY . .

# Expose the application port.
EXPOSE 8000

# Default command: run migrations and start the Django server.
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
