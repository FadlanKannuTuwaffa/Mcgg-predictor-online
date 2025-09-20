# Dockerfile (untuk backend FastAPI)
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Install build deps (psycopg2 / Postgres client)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
  --no-install-recommends && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# Copy the backend code
COPY backend/ /app/backend/

WORKDIR /app/backend
EXPOSE 8080

# Start command (gunakan uvicorn). Fly akan set PORT env otomatis.
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
