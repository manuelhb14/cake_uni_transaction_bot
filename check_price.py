from txns import Txn_bot

token_address = '0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82' #Example CAKE bsc-mainnet

quantity = 50*10**18
net = 'bsc-mainnet'
slippage = 5 #%
gas_price = 5*10**9 #Gwei, bsc-mainnet=5, eth-mainnet=https://www.gasnow.org/, eth-rinkeby=1
bot = Txn_bot(token_address, quantity, net, slippage, gas_price)
tokens = bot.get_amounts_out_buy()

#TODO: Add function to check price in ETH/BSC or BUSD/USDT