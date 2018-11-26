import sys
sys.path.append('./gen-py')

from kv import KVService as ThriftKVService

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from mamba import description, context, it
from expects import expect, equal

import json

test_doc_path = './data/test_doc.json'

try:
    with description('ThriftKV') as self:
        doc_id = ''
        with it('the create method is called and returns a mongo object id'):
            transport = TSocket.TSocket('0.0.0.0', 9090)
            transport = TTransport.TBufferedTransport(transport)
            protocol = TBinaryProtocol.TBinaryProtocol(transport)
            client = ThriftKVService.Client(protocol)
            transport.open()

            # Get thrift client and open transport protocol
            with open(test_doc_path) as f:
                global doc_id
                doc = f.read()
                doc_id = json.loads(client.create(doc))
                
                expect('$oid' in doc_id.keys())

            transport.close()

        with it('the read method is called and verified against the original string'):
            transport = TSocket.TSocket('0.0.0.0', 9090)
            transport = TTransport.TBufferedTransport(transport)
            protocol = TBinaryProtocol.TBinaryProtocol(transport)
            client = ThriftKVService.Client(protocol)
            transport.open()

            with open(test_doc_path) as f:
                doc = json.load(f)
                doc_from_kv = json.loads(client.read(json.dumps(doc_id)))
                for k,v in doc.items():
                    expect(v == doc_from_kv[k])

            transport.close()

        with it('the update method is called and verified'):
            transport = TSocket.TSocket('0.0.0.0', 9090)
            transport = TTransport.TBufferedTransport(transport)
            protocol = TBinaryProtocol.TBinaryProtocol(transport)
            client = ThriftKVService.Client(protocol)
            transport.open()

            new_key = 'new key'
            new_value = 'new value'
            doc_from_kv = json.loads(client.read(json.dumps(doc_id)))
            doc_from_kv[new_key] = new_value
            doc_from_kv = json.loads(client.update(json.dumps(doc_id), json.dumps(doc_from_kv)))
            expect(new_key in doc_from_kv.keys())
            expect(new_value in doc_from_kv.values())

            transport.close()

        with it('the delete_doc method is called and then the filter should find n on read'):
            transport = TSocket.TSocket('0.0.0.0', 9090)
            transport = TTransport.TBufferedTransport(transport)
            protocol = TBinaryProtocol.TBinaryProtocol(transport)
            client = ThriftKVService.Client(protocol)
            transport.open()

            client.delete_doc(json.dumps(doc_id))

            expect(client.read(json.dumps(doc_id)) == 'null')

            transport.close()

except Thrift.TException, tx:
    print str(tx)
