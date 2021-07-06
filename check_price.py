from txns import Txn_bot

token_address = '0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984' #Example UNI eth-mainnet
net = 'bsc-mainnet'

bot = Txn_bot(token_address, net)
print(bot.check_price_busd_usdc())


token_address = '0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82' #Example CAKE bsc-mainnet
net = 'bsc-mainnet'

bot = Txn_bot(token_address, net)
print(bot.check_price_busd_usdc())
