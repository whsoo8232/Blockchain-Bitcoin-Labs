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


    tokenAddress = "0x9eD9dBDd506ffD9c2d9A93d679109433E5a0d799"
    tokenAbi = "./source/myTest1.abi"

    web3 = polygon_connect_web3(network, apikey)

    myContract = polygon_get_contract(web3, tokenAddress, tokenAbi)
    
    amt = 10000
    polygon_token_airdrop_mint(web3, myContract, account1, pk1, account2, amt)
