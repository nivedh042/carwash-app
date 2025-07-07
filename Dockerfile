FROM python:3.11-slim

WORKDIR /app
COPY . .

# Debug: List files and permissions at build time
RUN ls -l /app

# Install requirements if you have a requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Debug: List files and permissions at container startup, then run the app
CMD ["/bin/sh", "-c", "ls -l /app; echo 'Starting app.py...'; python app.py"]
