# Using python 3.10 slim image as the base image
FROM python:3.10.7-slim

# Set working directory inside the container
WORKDIR /usr/src/myapp

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all remaining files into the container
COPY . .

# Expose the UI port (5001)
EXPOSE 5001

# Run the Flask UI application
CMD ["python", "app.py"]

