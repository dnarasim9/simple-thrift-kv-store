# start from base
FROM ubuntu:latest
MAINTAINER Ryan Haynes <rhaynesak@gmail.com>

# install system-wide deps for python and node
RUN apt-get -yqq update
RUN apt-get -yqq install python-pip python-dev curl mongodb-clients

## copy our application code
ADD thrift-kv /opt/thrift-kv
WORKDIR /opt/thrift-kv

## fetch app specific deps
RUN pip install -r requirements.txt

# expose port
EXPOSE 9090

# start app
CMD [ "python", "./app.py" ]
