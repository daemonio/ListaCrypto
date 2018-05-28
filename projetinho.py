#!/usr/bin/env python2.7

from uuid import getnode as get_mac
from iota import Iota, ProposedTransaction, ProposedBundle, Address, Tag, TryteString, Transaction
import sys

import hashlib
import os.path

class MyIOTA:
    def __init__(self, node, seed):
        self.node = node
        self.seed = seed
        self.api = False
        self._update = False
        self.transfers = []
        self._debug = False

        self.wallet = self.get_filename()

        self.addr_dict = {}

        self.min_weight_magnitude = 14

        self.api = Iota(self.node, self.seed)

        self.USED = True
        self.NOT_USED = False

    def get_addr_dict(self):
        return self.addr_dict

    def set_addr_dict(self, addr, value, used):
        self.addr_dict[addr] = (value, used)

    def s_addr(self, addr, n = 3):
        s_addr = str(addr)
        l = len(s_addr)

        return s_addr[:n]+'...'+s_addr[l-n:]

    def get_filename(self):
        h = hashlib.sha256()
        h.update(self.seed)
        filename = h.hexdigest()[:20]+'.txt'

        return filename

    def init_wallet(self):
        filename = self.wallet

        # file exists
        if os.path.isfile(filename):
            filefd = open(filename, 'r+')

            self.debug('Wallet file {0} exists. Opening it...'.format(filename))

            for line in filefd:
                line = line.rstrip('\n')

                addr, index, value, used = line.split(',')

                self.debug('reading from file: {0},{1},{2}'.format(self.s_addr(addr, 3), value, used))

                used = used == 'True'

                addr = Address(addr, key_index = int(index), security_level = 2)
                self.addr_dict[addr] = (int(index), int(value), used)

            filefd.close()
        else:
            filefd = open(filename, 'w')
            self.debug('Wallet file {0} doesnt exist. Creating it...'.format(filename))
            filefd.close()

    def is_empty_wallet(self):
        return len(self.addr_dict) == 0

    def get_fund_inputs(self, inputs):
        total_fund = 0

        for addr in inputs:
            index, value, used = self.addr_dict[addr]

            # TODO: abs. is this right?
            total_fund += abs(value)

        return total_fund

    def write_updates(self):
        filefd = open(self.wallet, 'w')

        self.debug('Writing (updating) wallet...')

        for addr in self.addr_dict:
            v = self.addr_dict[addr]

            line = 'Writing: {0},{1},{2},{3}\n'.format(self.s_addr(addr), v[0], v[1], v[2])
            self.debug(line)

            filefd.write('{0},{1},{2},{3}\n'.format(addr, v[0], v[1], v[2]))

        filefd.close()

    def update_wallet(self, input_fund, inputs, change_addr):
        copy_dict = self.addr_dict.copy()

        for addr in inputs:
            v = self.addr_dict[addr]
            #self.debug('Spending {0} from input {1}'.format(self.s_addr(addr), v))

            # Negative fund and used address
            new_value = (v[0], -v[1], not v[2])

            self.debug('Updating input address {0} to: {1}'.format(self.s_addr(addr), new_value))

            self.addr_dict[addr] = new_value

        change_fund = self.get_fund_inputs(inputs) - input_fund

        v = self.addr_dict[change_addr]
        change_value = (v[0], change_fund, self.NOT_USED)

        self.debug('Updating change address {0} to: {1}'.format(self.s_addr(change_addr), change_value))

        self.addr_dict[change_addr] = change_value

        self.write_updates()

    def enable_debug(self):
        self._debug = True

    def debug(self, msg):
        if self._debug:
            print '[+] Debug: ', msg

    def get_node_info(self):
        self.api.get_node_info()

    def make_addr_list(self, start_index, n):
        self.iota_assert(start_index >= 0 and n > 0, 'must be positive numbers. N should be at least 1.')

        result = self.api.get_new_addresses(index = start_index, count = n)
        addresses = result['addresses']

        for i in range(n):
            addr = addresses[i]
            value = self.get_addr_balance(addr)

            # TODO: Why always False
            self.addr_dict[addr] = (i, value, False)

    def get_addr_balance(self, addr):
        # TODO: addr is a list with just one element
        result = self.api.get_balances([addr])

        balance = result['balances']

        return (balance[0])

    def prepare_transfer(self, transfer_value, dest_addr, tag = 'DEFAULT', msg = 'DEFAULT'):
        # TODO: verify address (checksum)
        # TODO: use mi, gi, etc

        msg = TryteString.from_string(msg)

        txn = ProposedTransaction(address=Address(dest_addr),
                message=msg,
                tag=Tag(tag),
                value=transfer_value,
                )

        return txn

    def find_transactions(self):
        addr_list = []
        for e in self.addr_dict.items():
            addr = e[0]

            addr_list.append(addr)

        return self.api.findTransactions(addresses = addr_list)['hashes']

    def get_bundle(self, trans):
        return self.api.getBundles(transaction = trans)

    def get_latest_inclusion(self, addrl):
        return self.api.get_latest_inclusion(hashes = addrl)

    def get_total_fund(self):
        total_fund = 0

        for addr in self.addr_dict.items():
            # key and value from dict
            k, v = addr

            print k, v

            index, value, used = v

            #if not used:
            total_fund += value

        return total_fund

    def send_transfer(self, input_fund, inputs, outputs, change_addr):
        iota.debug('Sending {0} transactions, please wait...'.format(len(outputs)))

        #self.update_wallet(input_fund, inputs, change_addr)
        #return

        self.api.send_transfer(
                inputs=inputs,
                depth=7,
                transfers=outputs,
                change_address=change_addr,
                min_weight_magnitude=self.min_weight_magnitude)

        self.update_wallet(input_fund, inputs, change_addr)

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

    def get_info_transactions(self, transactions_hashes):
        txn_tuples = []

        for h in transactions_hashes:
            trytes = iota.get_trytes([h])
            txn = iota.get_transaction_from_trytes(trytes)

            (_, _, addr_t, value_t, tag_t, msg_t) = iota.get_transaction_fields(txn)

            txn_tuples.append((addr_t, value_t, tag_t, msg_t))
            #txn_tuples.append((tag_t, msg_t))

        return txn_tuples

    def get_inputs(self, fund, get_change_addr = False):
        # TODO: Zero fund
        fund_sum = 0
        addr_list = []
        change_addr = None

        for e in self.addr_dict.items():
            addr, v = e
            index, value, used = v

            if fund_sum < fund:
                #if value > 0 and not used:
                if value > 0 and used == self.NOT_USED:
                    fund_sum += value
                    iota.debug('Found request: {0}. Found address {1} with fund {2}.'.format(fund, iota.s_addr(addr), value))
                    addr_list.append(addr)

        if get_change_addr:
            for e in self.addr_dict.items():
                addr, v = e
                index, value, used = v

                if used == self.NOT_USED and addr not in addr_list:
                    change_addr = addr

                    iota.debug('Using {0} as change addr.'.format(iota.s_addr(addr)))
                return (addr_list, change_addr)

            # TODO
            self.iota_assert(True, 'No change addr available.')

        
        return addr_list

    def iota_assert(self, condition, msg):
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

def get_zero_transactions(filename, fileid, value, bufsize, dest_addr):
    txn_list = []
    index = 1

    buffer_msg = get_buffer_from_file(filename, bufsize)
    l = len(buffer_msg)

    for msg in buffer_msg:
        TAG = '{0}|{1}|{2}'.format(index, l, fileid)
        TAG = TryteString.from_string(TAG)

        txn = iota.prepare_transfer(dest_addr, value, TAG, msg)
        txn_list.append(txn)

        index += 1

    return txn_list

def save_to_file(filename, content):
    for (tag, msg) in sorted(content):
        print tag, msg

# Set your SEED.
SEED   = 'WXBTI9EVKNBEMBWMQUVOKALPQZGURKXQUUOZMGLIPIPU99RCYSPPIOQN9SJSPTDZVIIXKPRJQIVQARINL'
SEED1  = 'HRSBSSHTZRVRFYDVUYKLCAYHFWG9QQRRS9NZJQZQNUNUR9ZFPWUBI9HMMRWIS9TFCTTYRZVRDDIKUMLTK'

# Let's create our connection.
iota = MyIOTA('http://localhost:14265', SEED1)
iota.enable_debug()

iota.init_wallet()

if iota.is_empty_wallet():
    # Let's send some IOTAS. First we get an address with fund.
    # We generate 5 address. They will be saved to the addr_dict variable.
    iota.make_addr_list(start_index = 0, n = 5)

print iota.get_total_fund()
txn_list = iota.find_transactions()
for txn in iota.get_info_transactions(txn_list):
    addr_t, value_t, _, _ = txn

    print addr_t, value_t
sys.exit()

transfer_value = 500
dest_addr = Address('AXSJHWXGJMKMOS9LPZSATWDYRPTNVYAELDDWXMGTHOTLGWHRVDVZOBI9IQMELSEMMQKFVSNHYXYUWMZJBLRVJUPWEC')

inputs, change_addr = iota.get_inputs(transfer_value, get_change_addr = True)
output1 = iota.prepare_transfer(transfer_value, dest_addr, tag = 'TEST', msg = 'HELLO')

iota.send_transfer(transfer_value, inputs, [output1], change_addr)

sys.exit()
