FROM python:3.11.4-alpine3.18

RUN pip install cryptography adsbxcot

COPY *.pem /
COPY config.ini /

ENTRYPOINT ["adsbxcot"]