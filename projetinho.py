#!/usr/bin/env python

from uuid import getnode as get_mac
from iota import Iota, ProposedTransaction, ProposedBundle, Address, Tag, TryteString

#from iota import Iota
# Generate a random seed.
#api = Iota('http://localhost:14265')
SEED = 'BN9PCNCSGDIL9IWVVZQ9FKETVHQPKWWFXHYEKTQERPJXMEMUJRNWFDIHOJWUFUW9SUKNCUJASBGZHTVEL'
# Specify seed.
#api = Iota('http://localhost:14265', SEED)
#print(api.get_node_info())

mac = get_mac()
MACADDR = ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))

api = Iota('http://localhost:14265',seed = SEED)

ADDR = 'HJTABZOCLVVXDSMEIMXNPTCCMZGZEHJRWEOGIXEGVBDTDDYLITNFAA99MVAMGRGJHACZ9DDGPZESDCNNCKOUFFJDGX'

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
