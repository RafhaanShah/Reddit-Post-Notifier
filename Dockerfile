FROM python:3.13-slim

LABEL org.opencontainers.image.source="https://github.com/RafhaanShah/Reddit-Post-Notifier"

ENV PYTHONUNBUFFERED=1

RUN useradd -r -m python
USER python

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python", "app.py"]
