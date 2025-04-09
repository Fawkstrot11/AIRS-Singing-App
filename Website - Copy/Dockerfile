# Use a slim Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies including ffmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app source code
COPY . .

# Expose the port Cloud Run expects
EXPOSE 8080

# Run the Flask app with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app.app:app"]
