FROM python:3.9-alpine

ENV PYTHONUNBUFFERED 1

RUN adduser -D python
USER python

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

ENTRYPOINT ["python", "app.py"]
