FROM ubuntu:22.04

COPY requirements.txt requirements.txt

# Disable interactive package installation
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update \
    && apt install -y python3 python3-pip python3-tk git\
    && pip3 install -r requirements.txt \
