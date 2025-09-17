FROM python:3.13-slim AS build

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential gcc && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -r -m python

USER python

WORKDIR /build

COPY requirements.txt .

RUN pip wheel --no-cache-dir --wheel-dir /build/wheels -r requirements.txt


FROM python:3.13-slim

LABEL org.opencontainers.image.source="https://github.com/RafhaanShah/Reddit-Post-Notifier"

RUN useradd -r -m python

USER python

WORKDIR /app

COPY --from=build /build/wheels /app/wheels

RUN pip install --no-cache-dir /app/wheels/*

COPY . .

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "app.py"]
