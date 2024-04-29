from web3 import Web3, HTTPProvider
from web3.exceptions import TimeExhausted
import json
import requests
import sys, os
sys.path.insert(1, '../../../Token_modules/')
from ERC20_gnc import *
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv('/home/whsoo8232/Token-build/Management/.env')

    network = "amoy"
    apikey = os.getenv("INFURA_API_KEY")

    account1 = os.getenv("MY_TESTMAIN")
    pk1 = os.getenv("MY_TESTMAIN_PK")
    account2 = os.getenv("MY_TESTTEST")
    pk2 = os.getenv("MY_TESTTEST_PK")

    nftAddress = "0x33911321910b0F2b9766f59D241ddd88F0D7eFf1"
    nftAbi = "./source/TestNFT.abi"

    web3 = polygon_connect_web3(network, apikey)

    myContract = polygon_get_contract(web3, nftAddress, nftAbi)
    
    ipfsUri = "https://files.projectcafe.kr/media/ipfs/TestNFT/1.json"
    token_id = polygon_NFT_totalSuply(web3, myContract) + 1
    polygon_NFT_mint(web3, myContract, account1, pk1, account1, ipfsUri, token_id)
