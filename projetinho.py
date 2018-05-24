#!/usr/bin/env python2.7

from uuid import getnode as get_mac
from iota import Iota, ProposedTransaction, ProposedBundle, Address, Tag, TryteString, Transaction

#import json
import sys

class MyIOTA:
    def __init__(self, node, seed, transferfile = False):
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

            addr_list.append(str(addr))

        return addr_list

    def get_addr_balance(self, addr):
        # TODO: addr is a list with just one element
        result = self.api.get_balances([addr])

        balance = result['balances']

        return (balance[0])

    def get_first_addr_with_fund(self, fund, n):
        for i in range(1, n+1):
            addr_list = self.get_addr_list(i)

            b = self.get_addr_balance(addr_list[i])

            if b > fund:
                return (i, addr, b)

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
        #txn = Transaction.from_tryte_string(trytes)

        confirmed = str(txn.is_confirmed)
        timestamp = str(txn.timestamp)
        address   = str(txn.address)
        value     = str(txn.value)
        tag       = str(txn.tag)

        return (confirmed, timestamp, address, value, tag)

    #
    # "META" functions. Only used for tests.
    #
    def meta_check_if_got_paid(self, transactions_hashes, my_addr, value):
        # TODO: iterativo
        trytes = iota.get_trytes(transactions_hashes)
        txn = iota.get_transaction_from_trytes(trytes)

        (_, _, addr_t, value_t, _) = iota.get_transaction_fields(txn)

        if addr_t == my_addr and value_t == value:
            return True

        return False

        #print address, my_addr, value


#
# Main
#
SEED   = 'WXBTI9EVKNBEMBWMQUVOKALPQZGURKXQUUOZMGLIPIPU99RCYSPPIOQN9SJSPTDZVIIXKPRJQIVQARINL'
MYADDR = 'UXIKPLHDHSNTTVTMGP9RNK9CVRHXRNFFZVTPGPHVTZMOTT9TMINEVNZHVMRJEEWCNSZYNNNITFKSSJUOCTND9VVDQD'

iota = MyIOTA('http://localhost:14265', SEED)
iota.get_addr_balance(MYADDR)

hashes = iota.get_transfers_hashes_by_addr_list([MYADDR])

iota.meta_get_paid(hashes, MYADDR, 100)

sys.exit(0)

trytes = iota.get_trytes(hashes)

txn = iota.get_transaction_from_trytes(trytes)

print iota.get_transaction_fields(txn)

#timestamp = str(txn.timestamp)
#tag = str(txn.tag)
#address = str(txn.address)
#confirmed = str(txn.is_confirmed)
#value = str(txn.value)

#print dir(txn)
#print timestamp, tag, address, confirmed, value



#gt_result = api.get_trytes([txn_hash_as_bytes])
#trytes = str(gt_result['trytes'][0])
#txn = Transaction.from_tryte_string(trytes)
#timestamp = str(txn.timestamp)
#tag = str(txn.tag)
#address = str(txn.address)
#short_transaction_id = short_t_id_start_idx

#b = iota.get_bundle('BLGTNPDL9SYOQRKESABEAXIEILQKSFTOKPMR9DCSUAKWDTOBROTCY9SRHUWSRZCXFPHDJXCRCNNUZ9999')
#b = iota.get_bundle('OEKNZ9OYAIXRZTZ9AFXNBCPG9DCFPPMMNSEPCTOMDELIZUJAARLAUWVTXZEZDOZRTHCQBOVHSOXT99999')['transaction_hash']
#print b




#t = iota.get_transfers_hashes_by_addr_list([MYADDR])
#t = t['hashes']
#print iota.get_latest_inclusion(t)['states']

