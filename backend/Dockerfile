# Use official Python image from Docker Hub
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of your application
COPY . /app

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI application with autoreload
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
