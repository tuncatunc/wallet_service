from web3 import Web3
ETHEREUM_RPC_URL = os.environ["ETHEREUM_RPC_URL"]

web3 = Web3(Web3.HTTPProvider(ETHEREUM_RPC_URL))

# Transfer ethereum from account_1 to account_2
def transfer_eth(private_key1, account_1, account_2, amount):
    nonce = web3.eth.getTransactionCount(account_1)
    tx = {
        'nonce': nonce,
        'to': account_2,
        'value': web3.toWei(amount, 'ether'),
        'gas': 2000000,
        'gasPrice': web3.toWei('50', 'gwei')
    }
    signed_tx = web3.eth.account.sign_transaction(tx, private_key1)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    return web3.toHex(tx_hash)

def get_balance(address):
    return web3.eth.getBalance(address)