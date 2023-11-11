FROM python:3.11

WORKDIR /project
COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN apt-get update && \
    apt-get install -y \
        libsqlite3-dev
        