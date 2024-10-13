# Use Python İmage
FROM python:3.9-slim

# Create Workdirection
WORKDIR /app

# Copy&download requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy App files
COPY .. .

# Start APP
CMD ["python", "app.py"]
