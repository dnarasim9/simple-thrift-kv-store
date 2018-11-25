#!/bin/bash
docker stop mongo
docker stop thriftkv
docker network rm hct-net
