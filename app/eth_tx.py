from web3 import Web3
ganache_url = 'http://127.0.0.1:8545'
web3 = Web3(Web3.HTTPProvider(ganache_url))
# account_1 = '0xFa3b2B3D614C7B2A6cc41Ca9bD2A376452d1Ea7C'
# private_key1 = '0xebb9ee8852e944359ba1875e356915377ac89f1609465f50ca7aa81672428c1c'
# account_2 = '0x5269a466283199E24A81D129d55f21109260f51e'

# #get the nonce.  Prevents one from sending the transaction twice
# nonce = web3.eth.getTransactionCount(account_1)

# #build a transaction in a dictionary
# tx = {
#     'nonce': nonce,
#     'to': account_2,
#     'value': web3.toWei(1, 'ether'),
#     'gas': 2000000,
#     'gasPrice': web3.toWei('50', 'gwei')
# }

# #sign the transaction
# signed_tx = web3.eth.account.sign_transaction(tx, private_key1)

# #send transaction
# tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

# #get transaction hash
# print(web3.toHex(tx_hash))

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