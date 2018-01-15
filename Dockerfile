# Use an official Python runtime as a parent image
FROM python:2.7-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install all needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Start the Flask server
#CMD ["python", "main.py"]
CMD gunicorn --bind 0.0.0.0:$PORT main:app