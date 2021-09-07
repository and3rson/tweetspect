FROM python:3.7-alpine3.14

WORKDIR /home/tweetspect

ADD requirements ./requirements/

RUN apk add --virtual .deps alpine-sdk && \
    pip install -r requirements/prod.txt && \
    apk del .deps

COPY tweetspect ./tweetspect/

CMD gunicorn tweetspect.app:app -b 0.0.0.0:8000 --worker-class aiohttp.GunicornWebWorker
