# Dockerfile
FROM python:3.7

RUN apt-get update -qq && apt-get install -y gcc

# pyc no create.[-B]
# stdout, stderr unbuffered.[-u]
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD . /var/www/html
WORKDIR /var/www/html

RUN pip install --upgrade pip
RUN pip install -r requirements.txt