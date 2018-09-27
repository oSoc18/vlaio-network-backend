FROM python:3

WORKDIR /usr/src/app
ENV PYTHONUNBUFFERED 1
COPY . .
ENTRYPOINT /usr/src/app/startup.sh
