#!/bin/bash
docker stop mongo
docker stop thriftkv
docker network rm thriftkv-net
