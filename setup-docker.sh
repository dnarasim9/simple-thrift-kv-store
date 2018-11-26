#!/bin/bash

# generate the thrift bindinges
docker run -v "$PWD/thrift-kv:/data" thrift thrift -o /data --gen py /data/kv.thrift

# build the flask container
docker build -t rhaynes385/hc_thrifter .

# create the network
docker network create thriftkv-net

# start the mongo container
docker run --name mongo -d  --rm -p 27017:27017 --net thriftkv-net -v ~/work/data/:/data/db mongo

# start the thrift key value store container
docker run --name thriftkv -d --rm -p 9090:9090 --net thriftkv-net rhaynes385/hc_thrifter

# run integration tests
# docker exec -it thriftkv python integration-client.py
