FROM python:3.10.1

ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=wsgi.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean

RUN pip install --upgrade pip

COPY ./requirements.txt /requirements.txt

RUN pip install -r requirements.txt

COPY ./app /app
COPY  ./.env /.env
COPY ./migrations /migrations
COPY ./config.py /config.py
COPY ./wsgi.py /wsgi.py
