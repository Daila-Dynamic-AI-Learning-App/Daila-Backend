# Use an official Python runtime as a base image with version 3.8.10
FROM python:3.8.10

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Gunicorn will listen on (default is 8000)
EXPOSE 8000

# Specify the command to run Gunicorn with your Flask app
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
