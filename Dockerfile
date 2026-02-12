# =========================
# Build stage
# =========================
FROM python:3.13.5-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# =========================
# Runtime stage
# =========================
FROM python:3.13.5-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=builder /usr/local /usr/local

COPY src ./src

EXPOSE 8000

ENTRYPOINT ["fastapi", "run", "./src/main.py", "--host", "0.0.0.0", "--port", "8000"]
