FROM python:3.10-slim

# System deps for OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
      libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", \
     "--timeout", "120", "app:app"]
