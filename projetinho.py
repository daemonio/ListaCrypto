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
        self._debug = False

        self.min_weight_magnitude = 14

        self.api = Iota(self.node, self.seed)

    def setDebug(self, flag = False):
        self._debug = flag

    def debug(self, msg):
        if self._debug:
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

#    def get_first_addr_with_fund(self, fund, n):
#        for i in range(1, n):
#            addr_list = self.get_addr_list(i)
#
#            # First address is at 1 but indexing is at 0.
#            # Note that addr is type IOTA Address not string.
#            addr = addr_list[i-1]
#
#            b = self.get_addr_balance(addr)
#
#            if b > fund:
#                return (i, addr, b)
#
#        return (None, None, None)

    def attach_tangle(self, n, start_index = 1):
        # n is the number of address to attach. It starts with 1
        addr_and_value_list = []

        iota.debug('Attaching {0} addresses. Please wait...'.format(n))

        for i in range(start_index, n):
            addr_list = self.get_addr_list(i)

            # First address is at 1 but indexing is at 0.
            # Note that addr is type IOTA Address not string.
            addr = addr_list[i-1]

            b = self.get_addr_balance(addr)

            addr_and_value_list.append((addr, i, b))

        return addr_and_value_list

    def prepare_transfer(self, dest_addr, transfer_value, tag, msg):
        # TODO: verify address (checksum)
        # TODO: use mi, gi, etc
        msg = TryteString.from_string(msg)

        #print '------------', TryteString.from_string(msg)
        #message=TryteString.from_string(msg),

        txn = ProposedTransaction(address=Address(dest_addr),
                message=msg,
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

    def send_transfer(self, prepared_transfers, zero_value = False):
        iota.debug('Sending {0} transactions, please wait...'.format(len(prepared_transfers)))

        self.api.send_transfer(
                inputs=iota.get_inputs(zero_value),
                depth=7,
                transfers=prepared_transfers,
                #change_address=change_addy,
                min_weight_magnitude=self.min_weight_magnitude)

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
        #print dir(txn)

        confirmed = str(txn.is_confirmed)
        timestamp = str(txn.timestamp)
        address   = str(txn.address)
        value     = str(txn.value)
        message   = str(txn.signature_message_fragment)
        #message   = str(txn.message)
        tag       = str(txn.tag)

        return (confirmed, timestamp, address, value, tag, message)

    def get_values_of_transactions(self, transactions_hashes):
        txn_tuples = []

        for h in transactions_hashes:
            trytes = iota.get_trytes([h])
            txn = iota.get_transaction_from_trytes(trytes)

            (_, _, addr_t, value_t, tag_t, msg_t) = iota.get_transaction_fields(txn)

            #txn_tuples.append((addr_t, value_t, tag_t, msg_t))
            txn_tuples.append((addr_t, msg_t))

        return txn_tuples

    def get_inputs(self, addr_list, zero_value = False):
        # Transactions with zero value, just return the first address.
        if zero_value:
            addr, index, _ = addr_list[0]
            return Address(address, key_index = index, security_level = 2)

def my_assert(condition, msg):
    if not condition:
        print 'Error: ', msg
        sys.exit(-1)

def get_buffer_from_file(filename, bufsize):
    f = open(filename, 'r')

    buf = []
    
    for line in f:
        line = line.rstrip('\n')

        i = 0
        while i < len(line):
            if bufsize < len(line):
                j = bufsize
            else:
                j = len(line)

            buf.append(line[i:i+j])

            i = i + j

    return buf
    f.close()

def get_transactions_as_file_buffer(filename, value, bufsize, dest_addr):
    txn_list = []
    index = 0

    buffer_msg = get_buffer_from_file(filename, bufsize)
    l = len(buffer_msg)

    for msg in buffer_msg:
        TAG = '{0}|{1}|{2}'.format(filename, index, l)
        TAG = TryteString.from_string(TAG)

        txn = iota.prepare_transfer(dest_addr, value, TAG, msg)
        txn_list.append(txn)

    return txn_list


SEED   = 'WXBTI9EVKNBEMBWMQUVOKALPQZGURKXQUUOZMGLIPIPU99RCYSPPIOQN9SJSPTDZVIIXKPRJQIVQARINL'
#MYADDR = Address('UXIKPLHDHSNTTVTMGP9RNK9CVRHXRNFFZVTPGPHVTZMOTT9TMINEVNZHVMRJEEWCNSZYNNNITFKSSJUOCTND9VVDQD')
#DESTADDR = Address('QXMWVWPOEOBDCBZYMDXUBI9NKZOGQYCBSUAOLWJYHFACTIBMLYRSNQNSGTNNB9WZBMMU9HPYLOAYATWDDBZIWBAWPW')
DESTADDR = Address('AXSJHWXGJMKMOS9LPZSATWDYRPTNVYAELDDWXMGTHOTLGWHRVDVZOBI9IQMELSEMMQKFVSNHYXYUWMZJBLRVJUPWEC')

iota = MyIOTA('http://localhost:14265', SEED)
iota.setDebug(True)

txn_list = get_transactions_as_file_buffer('teste.txt', 0, 100, DESTADDR)

txn_list = iota.get_transfers_hashes_by_addr_list([DESTADDR])

for (addr, msg) in iota.get_values_of_transactions(txn_list):
    print TryteString.as_string(TryteString(msg))
    #print msg

print dir(TryteString)

sys.exit()

# tuple: (address, fund).
#addr_list = iota.attach_tangle(10, start_index = 1)

#txn_list = get_transactions_as_file_buffer('teste.txt', value = 0, bufsize = 500, dest_addr = DESTADDR)
#iota.send_transfer(txn_list, zero_value = True)
