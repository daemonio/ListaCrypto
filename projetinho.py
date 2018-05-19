#!/usr/bin/env python2.7

from uuid import getnode as get_mac
from iota import Iota, ProposedTransaction, ProposedBundle, Address, Tag, TryteString

#import json
import sys

class MyIOTA:
    def __init__(self, node, seed, transferfile = False):
        self.node = node
        self.seed = seed
        self.api = False
        self._update = False
        self.transfers = []
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
        # TODO: addr is a list with just one element
        result = self.api.get_balances(addr)

        balance = result['balances']

        return (balance[0])

    def get_first_addr_with_fund(self, fund, n):
        for i in range(1, n+1):
            addr = self.get_addr(i)

            b = self.get_balance(addr)

            if b > fund:
                return (i, addr[0], b)

        return (None, None, None)

    def prepare_transfer(self, dest_addr, transfer_value, msg, tag):
        # TODO: verify address (checksum)
        # TODO: use mi, gi, etc
        msg = msg.upper()
        tag = tag.upper()
        txn = ProposedTransaction(address=Address(dest_addr),
                message=TryteString.from_string(msg),
                tag=Tag(tag),
                value=transfer_value,
                )

        self.transfers.append((txn, True))

        return len(self.transfers)

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

    def send_all_transfers(self):
        sent_one = False

        transfers_bkp = self.transfers[:]
        for t in self.transfers:
            (addr, value, is_new_transaction) = (t[0].address, t[0].value, t[1])

            if is_new_transaction:
                print 'Sending {0} iotas to {1}...{2}'.format(t[0].value, \
                        t[0].address[:5], t[0].address[75:])

                sent_one = True

            transfers_bkp.append((t[0], False))

        if sent_one:
            self.transfers = transfers_bkp

SEED = 'WSHQRZICNFQUQPAPYWKFPWKTWWBPQNMTDNBYSGFZURGBWONDQEBPLNUXJVQTPYNFJKKTFATIVJTBSAWUX'
iota = MyIOTA('http://localhost:14265', SEED)

iota.update()

print iota.get_node_info()
#rint iota.get_balance(iota.get_addr(1))

print iota.get_addr_with_balance(100, 5)

ADDR1='UXIKPLHDHSNTTVTMGP9RNK9CVRHXRNFFZVTPGPHVTZMOTT9TMINEVNZHVMRJEEWCNSZYNNNITFKSSJUOCTND9VVDQD'
ADDR2='JUKTBTLFOITZWWLXNYENXLUCZKMAUAFXXRQRHDMNQQWGEWTGKALMXKCZWMPZWBKSVPJPMFQYPYGKEQYFAULGMOR9NA'
ADDR3='TQWYFTFBGQSZZQ9AWWCAMYGC9TYNTJXOPAZIPUDSMRKLWCPTPZKGN9NSPKWXSHTATBTPMDHIHCAHIYDL9BBJIQIWEX'
ADDR4='J9VGDTX9FSRTGSG9SHGEFDNQZUIB99XHJRGRRKBOBFEEBRKTNPANQKYYPXZSAIOMGLKBKVHJTVLPSOQZWCWPJVAND9'
ADDR5='PYZYINKAYUXGQUCATBHXUNLPZRNOZHHQZYLGICPNLZAMXGVXTT9JNCYYYTPWQPYLXFIAKULBCCGMPDQEYZSWQFDGOX'

iota.prepare_transfer(ADDR1, 100, 'msg', 'tag')
iota.prepare_transfer(ADDR2, 100, 'msg', 'tag')
iota.prepare_transfer(ADDR3, 100, 'msg', 'tag')
iota.prepare_transfer(ADDR4, 100, 'msg', 'tag')
iota.prepare_transfer(ADDR5, 100, 'msg', 'tag')

iota.send_all_transfers()
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
