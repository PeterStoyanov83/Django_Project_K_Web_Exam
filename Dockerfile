FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Collect static files (if needed)
RUN python manage.py collectstatic --noinput

# Start the Gunicorn server
CMD ["gunicorn", "project_k.wsgi:application", "--workers=4", "--bind=0.0.0.0:8000"]
