# os
import sys
import os
import subprocess

# time
from datetime import datetime
import time

# config
import configparser

# logging
import logging
from logging.handlers import RotatingFileHandler
from logging.handlers import TimedRotatingFileHandler

# web3
from web3 import Web3

import urllib
import json


def polygon_set_logger(python_pgm):
    #log settings
    logFormatter = logging.Formatter(fmt='[%(asctime)s.%(msecs)03d] [%(levelname)-8s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # file handler settings
    logHandler = logging.handlers.TimedRotatingFileHandler(filename=f'/home/whsoo8232/Token-build/ContractBase/logs/{python_pgm}.log', when='midnight', interval=1, encoding='utf-8')
    logHandler.setFormatter(logFormatter)

    #logger set
    logger = logging.getLogger()
    logger.addHandler(logHandler)

    return logger


def polygon_read_contractSource(contract_file):
    contract_source_code = None
    with open(contract_file, 'r') as file:
        contract_source_code = file.read()

    return contract_source_code


def polygon_write_contractSource(contract_file, contract_source_code):
    with open(contract_file, 'w') as file:
        file.write(contract_source_code)


def polygon_write_dotEnv(envFile, infuraKey, etherscanKey, ownerPK):
    f = open(envFile, 'w')

    f.write(f"INFURA_API_KEY='{infuraKey}'\n")
    f.write("BAOBAP_URL='https://api.baobab.klaytn.net:8651'\n")
    if etherscanKey == "":
        f.write("ETHERSCAN_API_KEY=\n")
    else:
        f.write("ETHERSCAN_API_KEY='{etherscanKey}'\n")

    f.write("PRIVATE_KEY1='"+ ownerPK + "'\n")

    f.close()


def polygon_read_hardhatConfig(hardhatConfig):
    f = open(hardhatConfig, 'r')
    lines = f.readlines()
    f.close()

    return lines


def polygon_write_hardhatConfig(hardhatConfig, lines, network):
    f = open(hardhatConfig, 'w')
    for line in lines:
        line = line.replace('localhost', network)
        f.write(line)
    f.close()


def polygon_make_deployScript(deployScriptSamp, deployScript, targetTokenName):
    f = open(deployScriptSamp, 'r')
    lines = f.readlines()
    f.close()
    f = open(deployScript, 'w')
    for line in lines:
        line = line.replace('tokenName', targetTokenName)
        f.write(line)
    f.close()


def polygon_deploy_contract(network, infuraKey, etherscanKey, ownerPK, tokenType, targetTokenName, targetSymbolName, targetAmount=None, logger=None, python_pgm=None):
    retCode = 0
    retMessage = ""

    command_exec = subprocess.Popen(["./deployContract.sh clean1"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, error = command_exec.communicate()
    command_exec.wait()

    retCode = command_exec.returncode
    if command_exec.returncode == 0:
        logger.debug(output)
        retMessage = output
    else:
        logger.error("%s failed %d %s %s" % (python_pgm, command_exec.returncode, output, error))
        retMessage = error


    sourceToken = ""
    envFile="../Upgradeable/.env"
    targetToken = "../Upgradeable/contracts/" + targetTokenName + ".sol"
    hardhatConfigSamp = "../Upgradeable/testConfig/hardhat.config.js.samp"
    hardhatConfig = "../Upgradeable/hardhat.config.js"
    deployScriptSamp = "../Upgradeable/testConfig/deployv1.js.samp"
    deployScript = "../Upgradeable/scripts/deployv1.js"
    jsonFile = "../Upgradeable/artifacts/contracts/" + targetTokenName + ".sol/" + targetTokenName + ".json"

    if tokenType == "ERC721" and targetAmount is None:
        sourceToken = "../tokenConfig/ERC721TokenName.sol"
        contract_source_code = polygon_read_contractSource(sourceToken).replace("ERC721TokenName", targetTokenName).replace("SymbolName", targetSymbolName);
    elif tokenType == "ERC20" and targetAmount is not None:
        sourceToken = "../tokenConfig/ERC20TokenName.sol"
        contract_source_code = polygon_read_contractSource(sourceToken).replace("ERC20TokenName", targetTokenName).replace("SymbolName", targetSymbolName).replace("initAmount", str(targetAmount));
    else:
        retCode = -1
        retMessage = f"tokenType({tokenType}), tokenName({targetTokenName}), symbol({targetSymbolName}), amount({targetAmount}) is invalid."
        return retCode, retMessage

    polygon_write_contractSource(targetToken, contract_source_code)

    polygon_write_dotEnv(envFile, infuraKey, etherscanKey, ownerPK)

    lines = polygon_read_hardhatConfig(hardhatConfigSamp)
    polygon_write_hardhatConfig(hardhatConfig, lines, network)

    polygon_make_deployScript(deployScriptSamp, deployScript, targetTokenName)

    command_exec = subprocess.Popen(["./deployContract.sh deploy1"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, error = command_exec.communicate()
    command_exec.wait()

    retCode = command_exec.returncode
    if command_exec.returncode == 0:
        logger.debug(output)
        retMessage = output
    else:
        logger.error("%s failed %d %s %s" % (python_pgm, command_exec.returncode, output, error))
        retMessage = error
        return retCode, retMessage

    contractAddress = ""
    lines = output.split("\n")
    for line in lines:
        if "deployed address to" in line:
            start = line.index("deployed address to") + 21
            contractAddress = line[start:]
    abiData = []
    byteCodeData = ""
    with open(jsonFile, 'r') as file:
        jsonData = json.load(file)
        abiData = jsonData['abi']
        byteCodeData = jsonData['bytecode']

    os.makedirs("../Upgradeable/backup/" + datetime.now().strftime("%Y_%m_%d") + "/" + network, exist_ok=True)  # 같은 폴더가 있어도 무시

    backupAbi = "../Upgradeable/backup/" + datetime.now().strftime("%Y_%m_%d") + "/" + network + "/" + targetTokenName + ".abi"

    with open(backupAbi, 'w', encoding='utf-8') as file:
        json.dump(abiData, file, indent="\t")

    backupContractFile = "../Upgradeable/backup/" + datetime.now().strftime("%Y_%m_%d") + "/" + network + "/" + targetTokenName + ".sol"
    polygon_write_contractSource(backupContractFile, contract_source_code)

    backupContractFile = "../Upgradeable/backup/" + datetime.now().strftime("%Y_%m_%d") + "/" + network + "/" + targetTokenName + ".addr"
    polygon_write_contractSource(backupContractFile, contractAddress)

    retMessage = targetTokenName + " deployed at " + contractAddress

    return retCode, retMessage

    
