from web3 import Web3, IPCProvider
from web3.middleware import geth_poa_middleware
import json
import time
import keys
import sys

class Txn_bot():
    def __init__(self, token_address, quantity, net, slippage, gas_price):
        self.net = net
        self.w3 = self.connect()
        print("Access to Infura node: {}".format((self.w3.isConnected())))
        self.address, self.private_key = self.set_address()
        print("Address: {}".format(self.address))
        print("Current balance of WETH/WBNB: {}".format(self.w3.fromWei(self.w3.eth.get_balance(self.address), 'ether')))
        self.token_address = Web3.toChecksumAddress(token_address)
        self.token_contract = self.set_token_contract()
        print("Current balance of {}: {}".format(self.token_contract.functions.symbol().call() ,self.token_contract.functions.balanceOf(self.address).call() / (10 ** self.token_contract.functions.decimals().call())))
        self.router_address, self.router = self.set_router()    # add router to access buy and sell txns, consult prices, etc
        self.quantity = quantity
        self.slippage = 1 - (slippage/100)
        self.gas_price = gas_price


    def connect(self):
        if self.net=="eth-mainnet":
            w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/{}".format(keys.infura_project_id)))
            w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        elif self.net=="eth-rinkeby":
            w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/{}".format(keys.infura_project_id)))
            w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        elif self.net=="bsc-mainnet":
            w3 = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org/"))
        # TODO: Add bsc-tesnet. Cake testing problems
        else:
            print("Not a valid network...\nSupported networks: eth-mainnet, eth-rinkeby, bsc-mainnet")
            sys.exit()
        return w3

    def set_address(self):
        if "eth" in self.net:
            return(keys.uniswap_address, keys.uniswap_private_key)
        else:
            return(keys.pancake_address, keys.pancake_private_key)

    def set_router(self):   #TODO: Refactor functions into shorter ones?
        if "eth" in self.net:
            router_address = Web3.toChecksumAddress("0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D")
            with open("./abis/IUniswapV2Router02.json") as f:
                contract_abi = json.load(f)['abi']
            router = self.w3.eth.contract(address=router_address, abi=contract_abi)
        else:
            router_address = Web3.toChecksumAddress("0x05fF2B0DB69458A0750badebc4f9e13aDd608C7F") # mainnet router
            with open("./abis/pancakeRouter.json") as f:
                contract_abi = json.load(f)['abi']
            router = self.w3.eth.contract(address=router_address, abi=contract_abi)
        return (router_address, router)

    def set_token_contract(self): #TODO: Refactor functions into shorter ones?
        if "eth" in self.net:
            token_address = Web3.toChecksumAddress(self.token_address)
            with open("./abis/erc20_abi.json") as f:
                contract_abi = json.load(f)
            token_contract = self.w3.eth.contract(address=token_address, abi=contract_abi)
        else:
            token_address = Web3.toChecksumAddress(self.token_address)
            with open("./abis/bep20_abi_token.json") as f:
                contract_abi = json.load(f)
            token_contract = self.w3.eth.contract(address=token_address, abi=contract_abi)
        return token_contract


    def get_amounts_out_buy(self):
        return self.router.functions.getAmountsOut(
            int(self.quantity * self.slippage),
            [self.router.functions.WETH().call(), self.token_address]
            ).call()

    def get_amounts_out_sell(self):
        return self.router.functions.getAmountsOut(
            self.token_contract.functions.balanceOf(self.address).call(),
            [self.token_address, self.router.functions.WETH().call()]
            ).call()

    def approve(self):
        txn = self.token_contract.functions.approve(
            self.router_address,
            2**256 - 1
        ).buildTransaction(
            {'from': self.address, 
            'gas': 250000,
            'gasPrice': self.gas_price,
            'nonce': self.w3.eth.getTransactionCount(self.address), 
            'value': 0}
            )
        
        signed_txn = self.w3.eth.account.sign_transaction(
            txn,
            self.private_key
        )
        txn = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        print(txn.hex())
        txn_receipt = self.w3.eth.waitForTransactionReceipt(txn)
        print(txn_receipt)

    def buy_token(self):
        txn = self.router.functions.swapExactETHForTokens(
            self.get_amounts_out_buy()[-1],
            [self.router.functions.WETH().call(), self.token_address], 
            bytes.fromhex(self.address[2:]), 
            int(time.time()) + 10 * 60 # 10 min limit
        ).buildTransaction(
            {'from': self.address, 
            'gas': 250000,
            'gasPrice': self.gas_price,
            'nonce': self.w3.eth.getTransactionCount(self.address), 
            'value': self.quantity}
            )

        signed_txn = self.w3.eth.account.sign_transaction(
            txn,
            self.private_key
        )

        txn = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        print(txn.hex())
        txn_receipt = self.w3.eth.waitForTransactionReceipt(txn)
        print(txn_receipt)

    def sell_token(self):
        txn = self.router.functions.swapExactTokensForETH(
            self.token_contract.functions.balanceOf(self.address).call(),
            int(self.get_amounts_out_sell()[-1] * self.slippage),
            [self.token_address, self.router.functions.WETH().call()], 
            bytes.fromhex(self.address[2:]), 
            int(time.time()) + 10 * 60 # 10 min limit
        ).buildTransaction(
            {'from': self.address, 
            'gas': 250000,
            'gasPrice': self.gas_price,
            'nonce': self.w3.eth.getTransactionCount(self.address), 
            'value': 0}
            )

        signed_txn = self.w3.eth.account.sign_transaction(
            txn,
            self.private_key
        )
        txn = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        print(txn.hex())
        txn_receipt = self.w3.eth.waitForTransactionReceipt(txn)
        print(txn_receipt)