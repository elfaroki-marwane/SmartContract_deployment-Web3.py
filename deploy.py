from solcx import compile_standard, install_solc
import json
from web3 import Web3


with open("./SimpleContract.sol", "r") as file:
    simple_contract_file = file.read()


print("Installing...")
install_solc("0.6.0")
# Solidity source code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleContract.sol": {"content": simple_contract_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)
# get the bytcode
bytecode = compiled_sol["contracts"]["SimpleContract.sol"]["SimpleContract"]["evm"][
    "bytecode"
]["object"]
# get abi
abi = compiled_sol["contracts"]["SimpleContract.sol"]["SimpleContract"]["abi"]
# connecting to ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 1337
my_address = "your address"
private_key = "0x+ your private key"
# creating the contract
SimpleContract = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)

transaction = SimpleContract.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)
# Signing the transaction
signed_transaction = w3.eth.account.sign_transaction(
    transaction, private_key=private_key
)
print("Deploying Contract!")
# Sending the transaction
transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
print(" Contract deployed!")
