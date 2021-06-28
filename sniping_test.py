from txns import Txn_bot

token_address = ""

quantity = 0.13*10**18
net = 'eth-mainnet'
slippage = 30 #%
gas_price = 160*10**9 #Gwei, bsc-mainnet=5, eth-mainnet=https://www.gasnow.org/, eth-rinkeby=1
bot = Txn_bot(token_address, quantity, net, slippage, gas_price)
tokens = bot.get_amounts_out_buy()
while (tokens==0):
    tokens = bot.get_amounts_out_buy()
bot.buy_token()

