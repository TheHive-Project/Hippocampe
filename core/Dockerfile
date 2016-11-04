#Hippocampe: Intel aggregator
#@author 2015 CERT-BDF <cert@banque-france.fr>
#@see The GNU Public License (GPL)
#
#This file is part of Hippocampe.
#
#Hippocampe is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 3 of the License, or
#(at your option) any later version.
#
#Hippocampe is distributed in the hope that it will be useful, but
#WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
#or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
#for more details.
#
#You should have received a copy of the GNU General Public License along
#with Hippocampe; if not, write to the Free Software Foundation, Inc.,
#59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#or see <http://www.gnu.org/licenses/>.
#

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
