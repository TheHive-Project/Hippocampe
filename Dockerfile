###################################################
# Lightweight Hippocampe container
###################################################

# Build the base from J8 Alpine
FROM openjdk:8-jre-alpine

RUN apk add --update --no-cache python \
    python-dev \
    py-pip \
    git \
    curl \
    nodejs \
    nodejs-npm

RUN npm install -g bower
RUN pip install --upgrade pip && \
    pip install apscheduler \
	Configparser \
    elasticsearch \
	flask \
	python-dateutil \
    requests

COPY ./core /opt/Hippocampe/core
COPY docker-entrypoint.sh /

RUN adduser hippo -D
RUN chown -R hippo:hippo /opt/Hippocampe /docker-entrypoint.sh

USER hippo

RUN cd /opt/Hippocampe/core/static && bower install

ENTRYPOINT /docker-entrypoint.sh
