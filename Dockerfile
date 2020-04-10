FROM ubuntu:18.04

WORKDIR /login

RUN apt-get update --fix-missing && \
    apt-get install -y --allow-unauthenticated -q python3-pip

RUN pip3 install \
    elasticsearch \
    redis \
    aiohttp

COPY . .

ENV PATH $PATH:/login/bin

CMD ['login']
