# syntax=docker/dockerfile:1

FROM python:3.10-alpine3.15
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./run-app.sh /app/run-app.sh
RUN chmod u+x ./run-app.sh

COPY ./src /app/src

CMD [ "/bin/sh", "./run-app.sh" ]
