import sys
sys.path.append('./gen-py')

from kv import KVService as ThriftKVService

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

import json

try:
    transport = TSocket.TSocket('0.0.0.0', 9090)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = ThriftKVService.Client(protocol)
    transport.open()

    doc = json.dumps({'i am a key': 'i am a value'})
    doc_id = client.create(doc)

    print client.read(doc_id)

    transport.close()

except Thrift.TException, tx:
    print str(tx)
