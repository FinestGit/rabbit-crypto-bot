# Rabbit Crypto Bot

## Description

_Rabbit Crypto Bot_ was designed around using Robinhood as the trading platform for crypto currency. This bot using RSI and MACD to make determinations of buying and selling a specific crypt that you may specify in the **config.py** file. Once you plug in all your information into this, the idea would be to just let this run and it will trade crypto for you. Always attempting to take a profit at any given time of a minimum of 1%, however this is dangerous and could leave you bag holding if not done correctly.

## How to Use Currently

To use this currently you must have Python 3.7.3 or higher which you can get here: [python.org](https://www.python.org/)
You will then have to install the following using pip:

- talib
- robin_stocks
- numpy

Once these are installed you will want to create a file called **testingConfig.py** and it should look something like this:

```
USERNAME="USERNAME"
PASSWORD="PASSWORD"
TRADING_ENABLED=False
TRADE_SYMBOL="SOMECOINSYMBOL"
RSI_PERIOD=14
RSI_OVERBOUGHT=70
RSI_OVERSOLD=30
PROFIT_PERCENT=1
MAXIMUM_CASH=100
```

Now simply run py test.py while in the folder that you cloned the repo into.

Future state you will not have to do most of this, but instead will just have to update the config.

## Future Updates

Working right now to improve how everything interacts with one another, at the moment it is not as user friendly as it could be.
