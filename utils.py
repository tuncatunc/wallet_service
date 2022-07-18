from web3 import Web3
ganache_url = 'http://127.0.0.1:8545'
web3 = Web3(Web3.HTTPProvider(ganache_url))
account_1 = '0xFa3b2B3D614C7B2A6cc41Ca9bD2A376452d1Ea7C'
private_key1 = '0xebb9ee8852e944359ba1875e356915377ac89f1609465f50ca7aa81672428c1c'
account_2 = '0xCb9916b5cEB0dfE96323271fdDb079de505ddEe4'

#get the nonce.  Prevents one from sending the transaction twice
nonce = web3.eth.getTransactionCount(account_1)

#build a transaction in a dictionary
tx = {
    'nonce': nonce,
    'to': account_2,
    'value': web3.toWei(10, 'ether'),
    'gas': 2000000,
    'gasPrice': web3.toWei('50', 'gwei')
}

#sign the transaction
signed_tx = web3.eth.account.sign_transaction(tx, private_key1)

#send transaction
tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

#get transaction hash
print(web3.toHex(tx_hash))
