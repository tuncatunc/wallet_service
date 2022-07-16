from py_crypto_hd_wallet import HdWalletBipFactory, HdWalletSaver, HdWalletBip44Coins, HdWalletBipWordsNum

hd_wallet_fact = HdWalletBipFactory(HdWalletBip44Coins.ETHEREUM)
hd_wallet = hd_wallet_fact.CreateRandom("eth_wallet", HdWalletBipWordsNum.WORDS_NUM_24)
hd_wallet.Generate(addr_num=3)
hd_wallet_dict = hd_wallet.ToDict()
mnemonic = hd_wallet.GetData('mnemonic')
HdWalletSaver(hd_wallet).SaveToFile("my_wallet.txt")

