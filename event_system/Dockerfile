# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application files
COPY . /app

# Event system does not expose a port, but RabbitMQ will handle its communication
CMD ["python", "listener.py"]
