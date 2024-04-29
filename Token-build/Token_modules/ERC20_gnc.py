from web3 import Web3, HTTPProvider
import json
import datetime
import os
import urllib
import time
import hashlib
import struct
from eth_account.messages import encode_defunct, encode_structured_data, defunct_hash_message


def polygon_connect_web3(connect_host, apikey):
    if connect_host is None:
        infura_url = "http://localhost:8545"
    elif connect_host == "polygon":
        infura_url = "https://polygon-mainnet.infura.io/v3/" + apikey
    elif connect_host == "amoy":
        infura_url = "https://rpc-amoy.polygon.technology"
    else:
        infura_url = "http://localhost:8545"
    web3 = Web3(Web3.HTTPProvider(infura_url))

    return web3


def polygon_scan_link(network, contract_address):
    if network == "polygon":
        url = f"https://polygonscan.com/address/{contract_address}"
    elif network == "amoy":
        url = f"https://www.oklink.com/amoy"
    else:
        url = "unknown"

    return url


def polygon_get_contract(web3, contractAddress, contractAbi):
    file = open(contractAbi, 'r', encoding='utf-8')
    contractaddress = web3.to_checksum_address(contractAddress)
    mycontract = web3.eth.contract(abi=file.read(), address=contractaddress)
	
    return mycontract


def polygon_read_abi(file_name):
    with open(file_name) as f:
	    info_json = json.load(f)

    return info_json["abi"]


def polygon_eth_get_balance(web3, account):
    account = web3.to_checksum_address(account)
    balance = web3.from_wei(web3.eth.get_balance(account), 'ether')
	
    return balance


def polygon_token_get_balance(web3, mycontract, account):
    token_balance = mycontract.functions.balanceOf(account).call()
    
    return token_balance


def polygon_token_totalSuply(web3, mycontract):
    total_token = mycontract.functions.totalSupply().call()
    print(total_token)
    
    return total_token


def polygon_token_approve(web3, mycontract, From, From_pk, To, value):
    From_add = web3.to_checksum_address(From)
    To_add = web3.to_checksum_address(To)
    nonce = web3.eth.get_transaction_count(From_add)
    gas_estimate = mycontract.functions.approve(To_add,value).estimate_gas({'from': From_add})
    lst = []
    print(gas_estimate)
    gas_price = web3.eth.gas_price
    print(gas_price)
    before_tx_fee = web3.from_wei(gas_estimate * gas_price, 'Ether')
    lst.append(before_tx_fee)
    print(before_tx_fee)
    tx = mycontract.functions.approve(To_add,value).build_transaction(
        {
            'from': From_add,
            'nonce': nonce,
            "gasPrice": gas_price
        }
    )
    signed_txn = web3.eth.account.sign_transaction(tx, From_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    gncHash = web3.eth.wait_for_transaction_receipt(txHash)
    after_tx_fee = web3.from_wei(gncHash.effectiveGasPrice * gncHash.gasUsed, 'Ether')
    lst.append(after_tx_fee)
    if before_tx_fee == after_tx_fee:
        lst.append('true')
    else:
        lst.append('false')
    
    return lst, gncHash


def polygon_token_mint(web3, mycontract, owner, owner_pk, value):
    owner_add = web3.to_checksum_address(owner)
    nonce = web3.eth.get_transaction_count(owner_add)
    amount = value * 10**mycontract.functions.decimals().call()
    gas_estimate = mycontract.functions.mint(owner_add,amount).estimate_gas({'from': owner_add})
    lst = []
    print(gas_estimate)
    gas_price = web3.eth.gas_price
    print(gas_price)
    before_tx_fee = web3.from_wei(gas_estimate * gas_price, 'Ether')
    lst.append(before_tx_fee)
    print(before_tx_fee)
    tx = mycontract.functions.mint(owner_add,amount).build_transaction(
        {
            'from': owner_add,
            'nonce': nonce,
            "gasPrice": gas_price
        }
    )
    print(tx)
    signed_txn = web3.eth.account.sign_transaction(tx, owner_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    gncHash = web3.eth.wait_for_transaction_receipt(txHash)
    after_tx_fee = web3.from_wei(gncHash.effectiveGasPrice * gncHash.gasUsed, 'Ether')
    lst.append(after_tx_fee)
    if before_tx_fee == after_tx_fee:
        lst.append('true')
    else:
        lst.append('false')
    
    return lst, gncHash


def polygon_token_airdrop_mint(web3, mycontract, From, From_pk, To, value):
    From_add = web3.to_checksum_address(From)
    To_add = web3.to_checksum_address(To)
    nonce = web3.eth.get_transaction_count(From_add)
    amount = value * 10**mycontract.functions.decimals().call()
    gas_estimate = mycontract.functions.mint(To_add,amount).estimate_gas({'from': From_add})
    lst = []
    print(gas_estimate)
    gas_price = web3.eth.gas_price
    print(gas_price)
    before_tx_fee = web3.from_wei(gas_estimate * gas_price, 'Ether')
    lst.append(before_tx_fee)
    print(before_tx_fee)
    tx = mycontract.functions.mint(To_add,amount).build_transaction(
        {
            'from': From_add,
            'nonce': nonce,
            "gasPrice": gas_price
        }
    )
    print(tx)
    signed_txn = web3.eth.account.sign_transaction(tx, From_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    gncHash = web3.eth.wait_for_transaction_receipt(txHash)
    after_tx_fee = web3.from_wei(gncHash.effectiveGasPrice * gncHash.gasUsed, 'Ether')
    lst.append(after_tx_fee)
    if before_tx_fee == after_tx_fee:
        lst.append('true')
    else:
        lst.append('false')

    return lst, gncHash


def polygon_token_burn(web3, mycontract, owner, owner_pk, value):
    owner_add = web3.to_checksum_address(owner)
    nonce = web3.eth.get_transaction_count(owner_add)
    amount = value * 10**mycontract.functions.decimals().call()
    gas_estimate = mycontract.functions.burn(amount).estimate_gas({'from': owner_add})
    lst = []
    print(gas_estimate)
    gas_price = web3.eth.gas_price
    print(gas_price)
    before_tx_fee = web3.from_wei(gas_estimate * gas_price, 'Ether')
    lst.append(before_tx_fee)
    print(before_tx_fee)
    tx = mycontract.functions.burn(amount).build_transaction(
        {
            'from': owner_add,
            'nonce': nonce,
            "gasPrice": gas_price
        }
    )
    signed_txn = web3.eth.account.sign_transaction(tx, owner_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    gncHash = web3.eth.wait_for_transaction_receipt(txHash)
    after_tx_fee = web3.from_wei(gncHash.effectiveGasPrice * gncHash.gasUsed, 'Ether')
    lst.append(after_tx_fee)
    if before_tx_fee == after_tx_fee:
        lst.append('true')
    else:
        lst.append('false')
    
    return lst, gncHash


def polygon_token_transferFrom(web3, mycontract, From, From_pk, To, value):
    From_add = web3.to_checksum_address(From)
    To_add = web3.to_checksum_address(To)
    amount = value * 10**mycontract.functions.decimals().call()
    nonce = web3.eth.get_transaction_count(From_add)
    gas_estimate = mycontract.functions.transfer(To_add,amount).estimate_gas({'from': From_add})
    lst = []
    print(gas_estimate)
    gas_price = web3.eth.gas_price
    print(gas_price)
    before_tx_fee = web3.from_wei(gas_estimate * gas_price, 'Ether')
    lst.append(before_tx_fee)
    print(before_tx_fee)
    tx = mycontract.functions.transfer(To_add,amount).build_transaction(
        {
            'from': From_add,
            'nonce': nonce,
            "gasPrice": gas_price
        }
    )
    signed_txn = web3.eth.account.sign_transaction(tx, From_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    gncHash = web3.eth.wait_for_transaction_receipt(txHash)
    after_tx_fee = web3.from_wei(gncHash.effectiveGasPrice * gncHash.gasUsed, 'Ether')
    lst.append(after_tx_fee)
    if before_tx_fee == after_tx_fee:
        lst.append('true')
    else:
        lst.append('false')

    return lst, gncHash


def polygon_verify_allowance(web3, mycontract, From, To):
     verify = mycontract.functions.allowance(From,To).call()
     
     print(verify)


def polygon_permit_hash(web3, mycontract, token_add, From, From_pk, To, deadline, amount):
    From_add = web3.to_checksum_address(From)
    To_add =  web3.to_checksum_address(To)
    nonce = mycontract.functions.nonces(From_add).call()
    contract_name = mycontract.functions.name().call()
    msg ={
    "domain": {
        "name": contract_name,
        "version": "1",
        "chainId": int(web3.net.version),
        "verifyingContract": token_add
    },
    "message": {
        "owner": From_add,
        "spender": To_add,
        "value": amount,
        "nonce": int(nonce),
        "deadline": deadline
    },
    "primaryType": "Permit",
    "types": {
        "EIP712Domain": [
        {
            "name": "name",
            "type": "string"
        },
        {
            "name": "version",
            "type": "string"
        },
        {
            "name": "chainId",
            "type": "uint256"
        },
        {
            "name": "verifyingContract",
            "type": "address"
        }
        ],
        "Permit": [
        {
            "name": "owner",
            "type": "address"
        },
        {
            "name": "spender",
            "type": "address"
        },
        {
            "name": "value",
            "type": "uint256"
        },
        {
            "name": "nonce",
            "type": "uint256"
        },
        {
            "name": "deadline",
            "type": "uint256"
        }
        ]
    }
    }
    new_msg = json.loads(json.dumps(msg))
    new_msg['domain']['version'] = str(new_msg['domain']['version'])
    encoded_data=encode_structured_data(new_msg)
    print(encoded_data)
    owner_pk = web3.eth.account.from_key(From_pk)
    signature = owner_pk.sign_message(encoded_data)
    print(signature)
    v = int(signature.v)
    r = to_32byte_hex(signature.r)
    s = to_32byte_hex(signature.s)
    confirm = web3.eth.account.recover_message(encoded_data ,signature = signature.signature)
    print(confirm)
    
    return v,r,s


def polygon_to_32byte_hex(val):
  
    return Web3.to_hex(Web3.to_bytes(val).rjust(32, b'\0'))


#def polygon_meta_transaction(web3, mycontract, token_add, From, From_pk, To, To_pk, reciepter, amt, fee, deadline):
    From_add = web3.to_checksum_address(From)
    To_add = web3.to_checksum_address(To)
    nonce = web3.eth.get_transaction_count(To_add)
    v,r,s = permit_hash(web3, mycontract, token_add, From_add, From_pk, To_add, deadline, amt+fee)
    gas_estimate = mycontract.functions.transferWithPermit(From_add, To_add, reciepter, amt, fee, deadline, v, r, s).estimate_gas({'from': To_add})
    lst = []
    print(gas_estimate)
    gas_price = web3.eth.gas_price
    print(gas_price)
    before_tx_fee = web3.from_wei(gas_estimate * gas_price, 'Ether')
    lst.append(before_tx_fee)
    print(before_tx_fee)
    tx = mycontract.functions.transferWithPermit(From, To, reciepter, amt, fee, deadline, v, r, s).build_transaction(
        {
            'from': To_add,
            'nonce': nonce,
            "gasPrice": gas_price
        }
    )
    signed_txn = web3.eth.account.sign_transaction(tx, To_pk)
    amtTxHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    gncHash = web3.eth.wait_for_transaction_receipt(amtTxHash)
    after_tx_fee = web3.from_wei(gncHash.effectiveGasPrice * gncHash.gasUsed, 'Ether')
    lst.append(after_tx_fee)
    if before_tx_fee == after_tx_fee:
        lst.append('true')
    else:
        lst.append('false')
    return lst, gncHash


def polygon_token_change_ownership(web3, mycontract, From, From_pk, To):
    From_add = web3.to_checksum_address(From)
    To_add = web3.to_checksum_address(To)
    nonce = web3.eth.get_transaction_count(From_add)
    lst = []
    gas_estimate = mycontract.functions.transferOwnership(To_add).estimate_gas({'from': From_add})
    lst.append(gas_estimate)
    gas_price = web3.eth.gas_price
    lst.append(gas_price)
    tx = mycontract.functions.transferOwnership(To_add).build_transaction(
        {
            'from': From_add,
            'nonce': nonce,
            'gasPrice': gas_price
        }
    )
    signed_txn = web3.eth.account.sign_transaction(tx, From_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    gncHash = web3.eth.wait_for_transaction_receipt(txHash)
    after_tx_fee = web3.from_wei(gncHash.effectiveGasPrice * gncHash.gasUsed, 'Ether')
    lst.append(after_tx_fee)

    return lst, gncHash
