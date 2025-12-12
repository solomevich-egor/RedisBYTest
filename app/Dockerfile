FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

EXPOSE 80

ADD requirements.txt /tmp/requirements.txt

RUN python -m pip install --upgrade -r /tmp/requirements.txt

ARG VERSION=0.0.0

COPY . /app

ENV MAX_WORKERS=1
ENV MODULE_NAME=src.main
