# Uniswap/PancakeSwap transaction bot

Bot to buy, sell, check price of token listed on Uniswap or PancakeSwap.

Will be added to PyPi in the future.

## How to use it

### Infura node

Create an account on [Infura](https://infura.io/) to create a **free** node to process all your transactions. **(Only necessary if you will use Uniswap)**

### Keys

Create a Python file called **keys.py** to store your Metamask information and your Infura project id.
Example:

```(python)
#Infura node
infura_project_id = ""

# Metamask keys
metamask_address = ""
metamask_private_key = ""
```

### Main file

You can see an example for buying a token on this [file](buy_example.py)

#### Explanation of the code

Import the Txn_bot object that executes all transactions.

```(python)
from txns import Txn_bot
```

Set the token address where you want to buy, sell, check price. You can check this on **[CoinMarketCap](https://coinmarketcap.com/)** or **[Coingecko](https://coingecko.com/)** by **searching the coin** and looking on **Contract**.
![Coingecko contract screenshot](/images/screenshot_coingecko.png)

```(python)
token_address = "0xf9ba5210f91d0474bd1e1dcdaec4c58e359aad85"
```

To create a transaction you need to specify four things:

- **Quantity**: The **amount** of tokens you want to buy/sell, if you want to only check prices quantity will be equal to zero.
    Decentralized Exchanges (DEX) use the **smallest units** of its network token (Ethereum(ETH) or Binance Coin(BNB)) which are called **Wei**.
    One Wei is 0.000000000000000001 ETH/BNB so if you want to make a transaction of 2.5 ETH/BNB you should specify 2.5x10^18.

```(python)
quantity = 0.13*10**18
```

- **Network**: Choose the network where your token is **located**.
    The options are **eth-mainnet** for **Uniswap**, or **bsc-mainnet** for **PancakeSwap**, if you want to **test** how the bot works you can also use **eth-rinkeby** network.

```(python)
net = 'eth-rinkeby'
```

- **Slippage**: Slippage is another characteristic of DEX to **reduce the number of failed transactions**.
    Slippage let's you specify how much difference from the estimated tokens recevied you actually get. For example if the estimated number of tokens you will receive is 100 and your slippage is at 10%, the transaction will be rejected if the tokens given to you is less than 90 (100-(100*10%) = 90). For more information about slippage you can read [this article on Medium](https://dexenetwork.medium.com/what-is-slippage-and-why-does-it-matter-uniswap-example-43e32d712651).
    A **higher slippage** means your **transaction is more likely to succeed** but be careful with **frontrunning**. Front-running in cryptocurrency trading is the illegal practice of using insider information to **make securities purchases** knowing other purchasers are going to buy the same currency and then **selling it at a higher price**. The **max** slippage is **49%**.

```(python)

slippage = 30 #%
```

-- **Gas Price**: Gas price is a **fee** to execute your transaction and it is measured in **Gwei**.
    The value of one Gwei is 0.000000001 ETH/BNB.
    The gas price you select on **PancakeSwap** will be normally **5 Gwei** (0.000000005 or 5x10^9 ETH/BNB). (You can use **higher gas prices** but **usually** on PancakeSwap is **not necessary**)
    On **Uniswap** the gas price oscillates **depending on the network congestion**. You can see the **real time prices** on **[GasNow website](https://www.gasnow.org/)** (For Uniswap I **suggest** using **Rapid or Fast** gas prices).
    The **higher gas price** you set the **faster your transaction will be completed**.

```(python)
gas_price = 1*10**9
```

Finally we can buy the token with the buy_token method that will return a transaction ID which can be tracked and reviewed on [EtherScan](https://etherscan.io/).

```(python)
bot = Txn_bot(token_address, quantity, net, slippage, gas_price)
bot.buy_token()
```

TODO: Add sell and check_price example codes.
