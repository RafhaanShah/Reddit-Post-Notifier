ARG BASE_IMAGE=python:3.13-alpine

FROM python:3.13-alpine

LABEL org.opencontainers.image.source="https://github.com/RafhaanShah/Reddit-Post-Notifier"

ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache gcc musl-dev python3-dev

RUN adduser -D python

USER python

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "app.py"]
