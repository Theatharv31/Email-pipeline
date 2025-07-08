# Use the official Python 3.11 slim image
FROM python:3.11-slim

# Set a working directory
WORKDIR /app

# Install system deps required by mysql client
RUN apt-get update \
     && apt-get install -y --no-install-recommends \
     build-essential \
     default-libmysqlclient-dev \
     && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything else
COPY . .

# Expose port and run Uvicorn
EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
