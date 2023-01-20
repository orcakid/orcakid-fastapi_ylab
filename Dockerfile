FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]