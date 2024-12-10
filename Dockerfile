FROM python:3.13.1-alpine3.21

RUN pip install cryptography adsbxcot

ENTRYPOINT ["adsbxcot"]
