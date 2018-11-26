#!/bin/bash

docker stop thriftkv

# generate the thrift bindinges
#docker run -v "$PWD/thrift-kv:/data" thrift thrift -o /data --gen py /data/kv.thrift

# build the flask container
docker build -t rhaynes385/hc_thrifter .

# start the thrift key value store container
docker run --name thriftkv -d --rm -p 9090:9090 --net thriftkv-net rhaynes385/hc_thrifter
# run integration tests
#docker exec -it thriftkv python client.py
