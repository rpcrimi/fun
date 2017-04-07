FROM       ubuntu:latest
MAINTAINER Robert Crimi <rpcrimi@gmail.com>

# Update apt-get sources AND install Python-dve
RUN apt-get update && apt-get install -y build-essential python-dev 
RUN apt-get install -y python-setuptools
RUN apt-get install -y python-pip

## Flask Extensions
RUN pip install flask-wtf
RUN pip install flask-bootstrap
RUN pip install flask-pymongo
RUN pip install flask-mail

EXPOSE 3000

COPY . /web
WORKDIR /web

ENTRYPOINT ["/usr/bin/python", "app.py"]