#!/usr/bin/env python2.7

from uuid import getnode as get_mac
from iota import Iota, ProposedTransaction, ProposedBundle, Address, Tag, TryteString, Transaction

#import json
import sys

class MyIOTA:
    def __init__(self, node, seed):
        self.node = node
        self.seed = seed
        self.api = False
        self._update = False
        self.transfers = []

        self.api = Iota(self.node, self.seed)

    def debug(self, msg, debug = False):
        print msg

    def get_node_info(self):
        self.api.get_node_info()

    def get_addr_list(self, n):
        addr_list = []

        if n < 1:
            return None

        result = self.api.get_new_addresses(count = n)
        addresses = result['addresses']

        for i in range(n):
            addr = addresses[i]

            addr_list.append(addr)

        # returns list of IOTA Address objects.
        return addr_list

    def get_addr_balance(self, addr):
        # TODO: addr is a list with just one element
        result = self.api.get_balances([addr])

        balance = result['balances']

        return (balance[0])

    def get_first_addr_with_fund(self, fund, n):
        for i in range(1, n):
            addr_list = self.get_addr_list(i)

            # First address is at 1 but indexing is at 0.
            # Note that addr is type IOTA Address not string.
            addr = addr_list[i-1]

            b = self.get_addr_balance(addr)

            if b > fund:
                return (i, addr, b)

        return (None, None, None)

    def prepare_transfer(self, dest_addr, transfer_value, msg, tag):
        # TODO: verify address (checksum)
        # TODO: use mi, gi, etc
        #msg = msg.upper()
        #tag = tag.upper()

        print '------------', TryteString.from_string(msg)
        #message=TryteString.from_string(msg),

        txn = ProposedTransaction(address=Address(dest_addr),
                message='AAAAAAAAAAAAAAa',
                tag=Tag(tag),
                value=transfer_value,
                )

        return txn

    def get_transfers_hashes_by_addr_list(self, addrl):
        return self.api.findTransactions(addresses = addrl)['hashes']

    def get_bundle(self, trans):
        return self.api.getBundles(transaction = trans)

    def get_latest_inclusion(self, addrl):
        return self.api.get_latest_inclusion(hashes = addrl)

    def _send_transfer(self, transfer, source_addr):
        api = Iota(iota_node, seed)
        api.send_transfer(
                inputs=get_inputs(),
                depth=7,
                transfers=prepared_transferes,
                change_address=change_addy,
                min_weight_magnitude=settings[0]['min_weight_magnitude']
                )

    def send_transfer(self, addr, index):
        pass

    def confirm_transactions(self):
        pass

    def send_all_transfers(self):
        pass

    def get_trytes(self, hashl):
        return self.api.get_trytes(hashl)['trytes'][0]

    def get_transaction_from_trytes(self, trytes):
        txn = Transaction.from_tryte_string(trytes)

        return txn

    def get_transaction_fields(self, txn):
        print dir(txn)

        confirmed = str(txn.is_confirmed)
        timestamp = str(txn.timestamp)
        address   = str(txn.address)
        value     = str(txn.value)
        #message   = str(txn.signature_message_fragment)
        message   = str(txn.message)
        tag       = str(txn.tag)

        return (confirmed, timestamp, address, value, tag, message)

    def get_values_of_transactions(self, transactions_hashes, my_addr):
        txn_tuples = []

        for h in transactions_hashes:
            pass
            trytes = iota.get_trytes(transactions_hashes)
            txn = iota.get_transaction_from_trytes(trytes)

            (_, _, addr_t, value_t, msg_t, _) = iota.get_transaction_fields(txn)

            txn_tuples.append((addr_t, value_t, msg_t))

        return txn_tuples

def my_assert(condition, msg):
    if not condition:
        print 'Error: ', msg
        sys.exit(-1)

#
# Main
#
SEED   = 'WXBTI9EVKNBEMBWMQUVOKALPQZGURKXQUUOZMGLIPIPU99RCYSPPIOQN9SJSPTDZVIIXKPRJQIVQARINL'
MYADDR = Address('UXIKPLHDHSNTTVTMGP9RNK9CVRHXRNFFZVTPGPHVTZMOTT9TMINEVNZHVMRJEEWCNSZYNNNITFKSSJUOCTND9VVDQD')
DESTADDR = Address('QXMWVWPOEOBDCBZYMDXUBI9NKZOGQYCBSUAOLWJYHFACTIBMLYRSNQNSGTNNB9WZBMMU9HPYLOAYATWDDBZIWBAWPW')

iota = MyIOTA('http://localhost:14265', SEED)

txn = iota.prepare_transfer(DESTADDR, 100, 'LMAO' , 'LMAO')

print iota.get_transaction_fields(txn)

sys.exit()

(_, MYADDR, _) = iota.get_first_addr_with_fund(10, 10)

print iota.get_addr_balance(MYADDR)

hashes = iota.get_transfers_hashes_by_addr_list([MYADDR])

my_assert(len(hashes) > 0, 'Nao existe transferencia associada ao endereco passado.')

print iota.get_values_of_transactions(hashes, MYADDR)
