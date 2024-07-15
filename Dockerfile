FROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt-get update && \
    apt-get install -y python3 python3-pip libmysqlclient-dev pkg-config

# Install MySQL
RUN apt-get install -y mysql-server

# Start
RUN service mysql start

WORKDIR /app

COPY requirements.txt /app/
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

COPY . /app/


EXPOSE 3000

CMD python3 ./App.py