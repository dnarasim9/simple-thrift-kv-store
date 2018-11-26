Thrift KV (Interview Programming Assessment
===

This is a trivial key value store. It uses mongodb as the backend and exposes a trivial CRUD api via thrift and python. There is code to run integration tests against the thrift kv server

#### Docker Setup

Getting the environment running is trivial with the docker implementation.

```
$ ./setup-docker.sh
```
This will execute the compilation of thrift python bindings in a seperate thrift container. Then the script will create a seperate container for both the mongodb daemon and the thrift server daemon.

##### Running Tests
```
docker exec -it thriftkv mamba integration-client.py
```
