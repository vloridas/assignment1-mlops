# Using python 3.10 slim image as the base image
FROM python:3.10.7-slim

# Defining working directory (within the container)
# and copy the requirements file. We will run the commands inside this directory
WORKDIR /usr/src/myapp

# Copy requirements.txt to the working directory
COPY requirements.txt .

# Install required python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port your app runs on
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]
