FROM python:3.7-alpine
LABEL maintainer="Lukas Pravda luky.pravda@gmail.com"

WORKDIR /app
COPY requirements.txt requirements.txt

RUN apk update
RUN apk add git build-base
RUN pip install -r requirements.txt

COPY . .

CMD /bin/sh -c
