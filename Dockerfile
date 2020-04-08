FROM ubuntu:bionic

WORKDIR /project/login

RUN apt-get install -y --allow-unauthenticated -q python3-pip

RUN pip3 install \
    elasticsearch \
    redis \
    aiohttp

ENV PATH $PATH:/project/login/bin

CMD ['login']