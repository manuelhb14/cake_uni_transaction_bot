from txns import Txn_bot
import time 

# token_address = '0xf9ba5210f91d0474bd1e1dcdaec4c58e359aad85' #Example UNI eth-rinkeby / eth-mainnet
# token_address = '0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82' #Example CAKE bsc-mainnet
# token_address = '0xe9e7cea3dedca5984780bafc599bd69add087d56' #BUSD bsc-mainnet

token_address = ""

quantity = 1*10**18
net = 'eth-mainnet'
slippage = 10 #%
gas_price = 5*10**9 #Gwei, bsc-mainnet=5, eth-mainnet=https://www.gasnow.org/, eth-rinkeby=1
bot = Txn_bot(token_address, quantity, net, slippage, gas_price)
# bot.buy_token()
# time.sleep(20)
bot.approve()
# time.sleep(20)
# bot.sell_token()
