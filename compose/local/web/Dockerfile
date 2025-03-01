FROM python:3.13.2

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

RUN pip install --upgrade pip

COPY ./requirements /requirements
RUN pip install -r /requirements/local.txt

COPY src /app