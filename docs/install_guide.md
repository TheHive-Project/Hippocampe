#Install Guide

##Intro
You will find bellow the installation instructions.
Don't want to install it ? You can use the docker version instead, check [this](#docker).
Check also the [tutorial](tutorial.md) for more details.

##Requirements

Hippocampe needs some external tools to work, you will find below the list of requirements:

+ JAVA (either [Oracle](http://www.webupd8.org/2014/03/oracle-java-8-stable-released-install.html) or [openJDK](http://openjdk.java.net/install/index.html), however we have noticed better performance with oracle)
+ [Elasticsearch **1.7**](https://www.elastic.co/guide/en/elasticsearch/reference/1.7/setup-repositories.html)
 + Some python libraries:
    + elasticsearch
    + Configparser
    + flask
    + python-dateutil
    + apscheduler

```
pip install elasticsearch Configparser netaddr flask python-dateutil apscheduler
```

##Configuration

Make sure in your elasticsearch's configuration (```/etc/elasticsearch/elasticsearch.yml```) to enable script & caching by adding the following lines:  
```
script.inline: on
script.indexed: on
threadpool.search.type: fixed
threadpool.search.size: 20
threadpool.search.queue_size: 10000
threadpool.search.type: cached
```

##Installation
* Clone or download the project
* Install the web dependencies with bower (https://bower.io/)
```
cd Hippocampe/core/static
bower install
```
* Start elasticsearch
```
service elasticsearch start
```
* run app.py script   
``` 
python Hippocampe/core/app.py
```
By default, Hippocampe is listening on port 5000.

##docker
If you just want to give it a try, you may want to use Hippocampe inside a docker:

```
cd Hippocampe/core
docker build -t hippocampe .
docker run -p 5000:5000 hippocampe 
```

Now Hippocampe is available on port 5000 and runs inside a docker. 
