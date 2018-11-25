import sys
sys.path.append('gen-py')

from bson.json_util import dumps, loads

from pymongo import MongoClient
from pymongo import ReturnDocument

from kv import KVService as ThriftKVService 

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

class ThriftKVHandler(object):
    def __init__(self, mongo_server='mongo', mongo_port=27017):
        self.log = {}
        self.client = MongoClient(mongo_server, mongo_port)
        self.db = self.client.thrift_kv_db
        self.collection = self.db.thrift_kv_collection

    def create(self, value):
        value = loads(value)
        return dumps(self.collection.insert_one(value).inserted_id)

    def read(self, obj_id):
        return dumps(self.collection.find_one({'_id' : loads(obj_id)}))

    def update(self, obj_id, value):
        obj_id = loads(obj_id)
        value = loads(value)
        ret = self.collection.find_one_and_replace({'_id': obj_id}, value,
                return_document=ReturnDocument.AFTER)
        return dumps(ret)

    def delete_doc(self, obj_id):
        self.collection.delete_one({'_id': loads(obj_id)})

if __name__ == "__main__":
    handler = ThriftKVHandler()
    processor = ThriftKVService.Processor(handler)
    transport = TSocket.TServerSocket(host='0.0.0.0', port=9090)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
    server.serve()
