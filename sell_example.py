from txns import Txn_bot

token_address = '0xe9e7cea3dedca5984780bafc599bd69add087d56' #BUSD bsc-mainnet

quantity = 1*10**18
net = 'bsc-mainnet'
slippage = 10 #%
gas_price = 5*10**9 #Gwei, bsc-mainnet=5, eth-mainnet=https://www.gasnow.org/, eth-rinkeby=1
bot = Txn_bot(token_address, quantity, net, slippage, gas_price)
tokens = bot.get_amounts_out_sell()
bot.sell_token()

#TODO: Add description to  README