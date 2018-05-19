#!/usr/bin/env python

from uuid import getnode as get_mac
from iota import Iota, ProposedTransaction, ProposedBundle, Address, Tag, TryteString

#import json
import sys

class MyIOTA:
    def __init__(self, node, seed):
        self.node = node
        self.seed = seed
        self.api = False
        self._update = False
        pass

    def debug(self, msg, debug = False):
        print msg

    def update(self, _debug = False):
        self._update = True
        self.api = Iota(self.node, self.seed)

    def is_updated(self):
        return self._update

    def get_node_info(self):
        if self.is_updated():
            #return json.dumps(self.api.get_node_info(), indent = 4)
            return self.api.get_node_info()
        else:
            return None

    def get_addr(self, n):
        addr_list = []

        if n < 1:
            return None

        result = self.api.get_new_addresses(count = n)
        addresses = result['addresses']

        for i in range(n):
            addr = addresses[i]

            addr_list.append(str(addr))

        return addr_list

    def get_balance(self, addr):
        result = self.api.get_balances(addr)

        balance = result['balances']

        return (balance[0])

    def get_addr_with_balance(self, balance, n):
        for i in range(1, n+1):
            addr = self.get_addr(i)

            b = self.get_balance(addr)

            if b > balance:
                return (addr, b)

        return (None, None)

    def transfer(self, addr):
        pass

    def toTrite(self, strdata):
        pass

SEED = '9ZWG9PYDMWDPUZ9LOXZPIYCKZFOBAOEFPDYZXGHOXTLV9DWYFSBREURIMWPZMJZWV9RHUPUAQTBKXTIAN'
iota = MyIOTA('http://localhost:14265', SEED)

iota.update()

print iota.get_node_info()
#rint iota.get_balance(iota.get_addr(1))

print iota.get_addr_with_balance(100, 5)

sys.exit()

#from iota import Iota
# Generate a random seed.
#api = Iota('http://localhost:14265')
# Specify seed.
#api = Iota('http://localhost:14265', SEED)
#print(api.get_node_info())

#mac = get_mac()
#MACADDR = ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))

SEED = '9ZWG9PYDMWDPUZ9LOXZPIYCKZFOBAOEFPDYZXGHOXTLV9DWYFSBREURIMWPZMJZWV9RHUPUAQTBKXTIAN'
api = Iota('http://localhost:14265',seed = SEED)

ADDR = 'AJGNCDNEUOAHBSRVREGTMV9QLEQUX9CIJFZNOCPGW9UFJSVGMVQVCX9VCAJTEGGSZOAGONBAWRDJRSBWDGC9RZSSLW'

print api.get_node_info()
print '----------------'
print

#print dir(api)

api.get_balances(SEED)

sys.exit(0)

output = ProposedTransaction(
    # receiving address of the transfer
    address = Address(ADDR),

    # Amount of Iota you want to send
    value = 1,

    # Optional Tag (27-trytes)
    tag = Tag(b'HELLO9WORLD'),

    # Message (2187-trytes)
    message = TryteString.from_string('Hello world!')
    )

bundle = ProposedBundle()

bundle.add_transaction(output)

prepared_bundle = api.prepare_transfer(bundle)
