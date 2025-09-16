ARG BASE_IMAGE=python:3.13-alpine

FROM python:3.13-alpine

LABEL org.opencontainers.image.source="https://github.com/RafhaanShah/Reddit-Post-Notifier"

ENV PYTHONUNBUFFERED=1

# dependency of requirements.txt
RUN apk add --no-cache py3-ruamel.yaml

RUN adduser -D python

USER python

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "app.py"]
