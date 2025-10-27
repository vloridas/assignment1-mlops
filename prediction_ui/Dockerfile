# prediction_ui/Dockerfile
FROM python:3.10-slim

WORKDIR /app

# If you add system deps later, install them here (e.g., gcc) then clean up

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=5001
EXPOSE 5001
CMD ["python", "app.py"]
