FROM alpine:latest

LABEL maintainer="LSS"

RUN apk update && apk upgrade --available && apk add --update python3 && apk add py3-pip && pip install requests pyyaml
RUN mkdir /home/pgInt && cd /home/pgInt && touch __init__.py

COPY main.py pgint.py conf.yaml /home/pgInt/
