FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade setuptools

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt


COPY . ./app

EXPOSE 8000













# FROM python:3.10-slim

# WORKDIR /app

# ENV PYTHONDONTWRITEBYTECODE 1

# ENV PYTHONUNBUFFERED 1

# COPY requirements.txt .

# RUN apt-get update \
#     && apt-get -y install libpq-dev gcc \
#     && pip install psycopg2

# RUN pip install -r requirements.txt

# COPY . .

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
