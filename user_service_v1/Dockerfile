# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application files
COPY . /app

# Expose the service port
EXPOSE 5001

# Command to run the service
CMD ["python", "app.py"]