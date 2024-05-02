from bitcoin_module import *

if __name__ == "__main__":
    # 	db_uri='mysql://bitcoinlib:12345!~@223.194.46.212:3306/bitcoinlib'
    db_uri = None

    wallet_name = "whsoo8232"
    #utxos = get_wallet_utxos(wallet_name)
    #print(utxos)
    
    send_address = "mjCFqXMTMPp3Ki2XmYTNxkRvuGX39i9Wbw"
    recv_addresses = ["mnDoVbd9SBWtP4fyYLf8AzMQMEj65QGFiz"]
    amt = [0.00001]

    transaction, tx = send_transaction(
        wallet_name, send_address, recv_addresses, amt, db_uri
    )
    print(f"transaction.txid=[{transaction.txid}]")
    http_url = "https://mempool.space/ko/testnet/tx/%s" % tx
    print(f"http_url=[{http_url}]")
    
