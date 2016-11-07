
###################################################
# Dockerfile to build hippocampe container images
# Based on Ubuntu
###################################################

# set the base image to ubuntu
FROM elasticsearch:1.7

# File Author / Maintener
MAINTAINER cert-bdf

########### BEGIN INSTALLATION ####################

RUN apt-get update

### Python libraries ###
RUN apt-get install -y python-pip libpython2.7-dev

RUN  pip install elasticsearch \
	Configparser \
	flask \
	python-dateutil \
	apscheduler

COPY . /opt/Hippocampe/core

######### INSTALLATION END #######################

######### Configuration    #######################
RUN  mkdir -p /opt/elasticsearch/data /opt/elasticsearch/logs

#fix apscheduler error
RUN pip install setuptools --upgrade

#Does not seem to work
#RUN chown -R elasticsearch:elasticsearch /opt/elasticsearch/data/ /opt/elasticsearch/logs


VOLUME ["/opt/elasticsearch/data", "/opt/elasticsearch/logs", "/etc/elasticsearch", "/opt/Hippocampe/core/conf/feeds", "/opt/Hippocampe/core/conf/auth", "/opt/Hippocampe/core/conf/hippo", "/opt/Hippocampe/core/logs"]

#flask api network
#$HOSTPORT:$CONTAINERPORT
EXPOSE 5000:5000

######### START APPLICATION ######################

WORKDIR /opt/Hippocampe/core

COPY docker-entrypoint /
ENTRYPOINT /docker-entrypoint
######### APPLICATION END #######################
