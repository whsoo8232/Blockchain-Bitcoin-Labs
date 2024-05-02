from bitcoinlib.keys import *
from bitcoinlib.wallets import *
from bitcoinlib.services.services import *
from bitcoinlib.transactions import *


class BitcoinError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


def send_transaction(wallet_name, send_address, recv_addresses, send_amts, db_uri=None):
    send_wallet = Wallet(wallet_name, db_uri)
    wallet_json = send_wallet.as_dict()
    wallet_network = wallet_json["main_network"]
    witness_type = wallet_json["witness_type"]
    dbs_uri = db_uri
    version = 2

    key_addresses = send_wallet.keys_addresses()
    for index in range(0, len(key_addresses)):
        hdkey = HDKey(key_addresses[index].wif)
        wif = key_addresses[index].wif
        if send_address == hdkey.address():
            break
    if send_address != hdkey.address():
        raise BitcoinError(
            "error address[%s] is not in wallet_name[%s]" & (send_address, wallet_name)
        )

    service = Service(network=wallet_network)

    try_cnt = 3
    balance = service.getbalance(hdkey.address())
    for i in range(1, try_cnt):
        if balance != 0:
            break
        balance = service.getbalance(hdkey.address())

    total_send = 0
    for index in range(0, len(send_amts)):
        total_send += int(send_amts[index] * 1e8)

    send_wallet.transactions_update()
    send_wallet.utxos_update()
    utxos = service.getutxos(hdkey.address())
    print(utxos)
    if not utxos:
        raise BitcoinError("%d utxo's found" % len(utxos))

    fee_amt = service.estimatefee(1008)

    total_sum = 0
    inputs = []
    for index in range(0, len(utxos)):
        total_sum += utxos[index]["value"]
        input = Input(
            prev_txid=utxos[index]["txid"],
            output_n=utxos[index]["output_n"],
            keys=hdkey.public(),
            network=wallet_network,
            value=utxos[index]["value"],
            witness_type=witness_type,
        )
        inputs.append(input)
        if total_sum > (total_send + fee_amt):
            break

    transaction = Transaction(
        inputs, network=wallet_network, witness_type=witness_type, version=version
    )

    for number in range(len(recv_addresses)):
        transaction.add_output(int(send_amts[number] * 1e8), recv_addresses[number])

    transaction.fee_per_kb = 0.00001
    fee_amt = int(transaction.calculate_fee())
    fee_amt = fee_amt * 1.5

    if balance < (total_send + fee_amt):
        raise BitcoinError(f"send_amt[{total_send}] is grater than balance[{balance}]")
    outChange = int(total_sum - total_send - fee_amt)
    transaction.add_output(outChange, send_address)

    transaction.sign(hdkey)
    tx = service.sendrawtransaction(transaction.raw_hex())

    return transaction, tx