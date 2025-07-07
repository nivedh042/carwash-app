FROM python:3.11-slim

WORKDIR /app
COPY . .

# Install requirements if you have a requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Example: run your main app (adjust if needed)
CMD ["python", "app.py"]
