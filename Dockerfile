ARG BASE_IMAGE=python:3.13-slim

FROM ${BASE_IMAGE} AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip wheel --no-cache-dir --no-deps -r requirements.txt -w /wheels


FROM ${BASE_IMAGE}

LABEL org.opencontainers.image.source="https://github.com/RafhaanShah/Reddit-Post-Notifier"

ENV PYTHONUNBUFFERED=1

RUN useradd -r -m python

USER python

WORKDIR /app

COPY --from=builder /wheels /wheels

RUN pip install --no-cache-dir /wheels/*

COPY . .

ENTRYPOINT ["python", "app.py"]
