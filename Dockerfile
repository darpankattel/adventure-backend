# Use official Python image
FROM python:3.10

RUN apt-get update && apt-get install -y libpq-dev

# Set the working directory in the container
WORKDIR /app

# Copy requirements file
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn separately
RUN pip install gunicorn python-dotenv

# Copy the entire Django project
COPY . .

# Set environment variables (optional, or use .env file)
ENV PYTHONUNBUFFERED=1

# Run migrations and collect static files before starting server
RUN python manage.py makemigrations && python manage.py migrate
RUN python manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Start Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi:application"]
