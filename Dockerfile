FROM python:3.8-slim-buster

WORKDIR /app

COPY challenge-job.py challenge-job.py


RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2 && pip install redis && pip install schedule

CMD [ "python3","./challenge-job.py" ]

