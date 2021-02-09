import time
import config as cfg
import robin_stocks as r
import talib
import numpy
import sys
import signal
import math
import datetime

class coin:
    purchasedPrice = 0.0
    numHeld = 0.0
    numBought = 0.0
    name = ""
    lastBuyOrderID = ""
    lastSellOrderID = ""
    boughtTime = ""

    def __init__(self, name=""):
        self.name = name
        self.purchasedPrice = 0.0
        self.numHeld = 0.0
        self.numBought = 0.0
        self.lastBuyOrderID = ""
        self.lastSellOrderID = ""
        self.boughtTime = ""

class bot:
    tradesEnabled = False
    rsiWindow = 0
    boughtIn = False
    rsiOverbought = 0
    rsiOversold = 0
    minCoinIncrement = 0.00
    minPriceIncrement = 0.00
    minOrderSize = 0.00
    coinTrend = []

    def __init__(self):
        self.loadConfig()

        Result = r.login(self.rh_user, self.rh_pw, 86400, by_sms=True)
    
    def loadConfig(self):
        print("\nLoading Config...")
        self.tradesEnabled = cfg.TRADING_ENABLED
        self.rsiWindow = cfg.RSI_PERIOD
        self.rsiOverbought = cfg.RSI_OVERBOUGHT
        self.rsiOversold = cfg.RSI_OVERSOLD
        self.rh_user = cfg.USERNAME
        self.rh_pw = cfg.PASSWORD
        self.coin = coin(cfg.TRADE_SYMBOL)
        print("\n")
    
    def getCurrentPrice(self):
        try:
            result = r.get_crypto_quote(self.coin.name)
        except:
            print("Problem retrieving crypto quote")
            return
        return float(result['mark_price'])
    
    def getIncrements(self):
        try:
            result = r.get_crypto_info(self.coin.name)
            self.minCoinIncrement = float(result['min_order_quantity_increment'])
            self.minPriceIncrement = float(result['min_order_price_increment'])
            self.minOrderSize = float(result['min_order_size'])
        except:
            print("Problem getting crypto information")
    
    def getCash(self):
        reserve = 0.00
        try:
            me = r.load_account_profile()
            cash = float(me['portfolio_cash'])
        except:
            print("Issue retrieving cash on hand amount")
            return -1.0
        
        if cash - reserve < 0.0:
            return 0.0
        else:
            return cash - reserve

    def getBuyingPower(self, cash, price):
        buyable_qty = float(cash / price)
        buyable_qty = self.roundDown(buyable_qty, self.minCoinIncrement)
        if buyable_qty > self.minOrderSize:
            return buyable_qty
        else:
            return 0
    
    def getProfitability(self):
        price = self.getCurrentPrice()
        total_sale = self.coin.numBought * price
        if total_sale > 0.01:
            profit_margin = total_sale - (self.coin.purchasedPrice * self.coin.numBought)
            if profit_margin > 0.01:
                print("Profitable")
                return True
            else:
                print("Profit margin too small, cancelling sale")
                return False
        else:
            print("Not making a profit, cancelling sale")
            return False

    def buyComplete(self):
        try:
            result = r.get_crypto_order_info(self.coin.lastBuyOrderID)
            state = result['state']
            if state == 'filled':
                return True
            else:
                return False
        except:
            print("Could not get order info")
            return False
    
    def sellComplete(self):
        try:
            result = r.get_crypto_order_info(self.coin.lastSellOrderID)
            state = result['state']
            if state == 'filled':
                return True
            else:
                return False
        except:
            print("Could not get order info")
            return False
    
    def cancelBuy(self):
        try:
            r.cancel_crypto_order(self.coin.lastBuyOrderID)
            return 0
        except:
            print("Failed to cancel, retrying")
            return -1
    
    def buy(self):
        availableCash = self.getCash()
        if availableCash == -1:
            print("Got an exception checking for available cash, cancelling buy.")
            return
        else:
            if self.tradesEnabled == True:
                try:
                    price = self.getCurrentPrice()
                    buyable_qty = self.getBuyingPower(availableCash, price)
                    if buyable_qty > 0:
                        try:
                            print("Buying")
                            result = r.order_buy_crypto_limit(self.coin.name, buyable_qty, price)
                            self.coin.purchasedPrice = price
                            self.coin.numBought = buyable_qty
                            self.coin.lastBuyOrderID = result['id']
                            self.coin.numHeld = self.coin.numBought + self.coin.numHeld
                            self.coin.boughtTime = str(datetime.datetime.now())
                        except:
                            print("Error buying, cancelling buy.")
                            return
                    else:
                        print("Need more funds")
                        return
                except:
                    print("Error getting quote for buy, cancelling buy.")
                    return
            return

    
    def sell(self):
        if self.coin.numBought <= 0:
            print("No coins to sell")
            return
        if self.tradesEnabled == True:
            if self.getProfitability():
                price = self.getCurrentPrice()
                sellable_qty = self.coin.numBought
                if sellable_qty > 0:
                    try:
                        print("Selling")
                        print("Sold {} {} @ {}".format(self.coin.numBought, self.coin.name, price))
                        result = r.order_sell_crypto_limit(self.coin.name, sellable_qty, price)
                        self.coin.purchasedPrice = 0.0
                        self.coin.numBought = 0.0
                        self.coin.lastBuyOrderID = ''
                        self.coin.numHeld = self.coin.numHeld - self.coin.numBought
                        self.coin.boughtTime = ''
                        self.coin.lastSellOrderID = result['id']
                    except:
                        print("Error selling, cancelling sale.")
                        return
            else:
                print("Not Profitable Holding")
        return
    
    def train(self):
        try:
            training_data = r.get_crypto_historicals(symbol=self.coin.name, interval='15second', span='hour', bounds='24_7', info='close_price')
            for data in training_data:
                self.coinTrend.append(float(data))
        except:
            print("Problem fetching training data")
            return
    
    def killBot(self, sig, frame):
        print('Exiting...')
        r.logout()
        sys.exit(0)
    
    def roundDown(self, x, a):
        return math.floor(x/a) * a
    
    def runBot(self):
        self.train()
        self.getIncrements()

        while True:
            self.coinTrend.append(self.getCurrentPrice())
            
            now = datetime.datetime.now()

            if len(self.coinTrend) > self.rsiWindow:
                np_closes = numpy.array(self.coinTrend)
                rsi = talib.RSI(np_closes, self.rsiWindow)
                macd, macdsignal, macdhist = talib.MACD(np_closes)
                last_macd = macd[-1]
                last_macdsignal = macdsignal[-1]
                last_macdhist = macdhist[-1]
                last_rsi = rsi[-1]
                print("Current rsi {}".format(last_rsi))
                print("Current macd {}".format(last_macd))
                print("Current macd signal {}".format(last_macdsignal))
                print("Current macd histogram {}".format(last_macdhist))

                if self.coin.lastBuyOrderID != '' and self.boughtIn == False:
                    if(self.buyComplete()):
                        print("Buy Completed!")
                        print("Bought {} {} @ {}".format(self.coin.numBought, self.coin.name, self.coin.purchasedPrice))
                        self.boughtIn = True
                    else:
                        dt_timeBought = datetime.datetime.strptime(self.coin.boughtTime, '%Y-%m-%d %H:%M:%S.%f')
                        timeDiffBuyOrder = now - dt_timeBought

                        if (timeDiffBuyOrder.total_seconds() > (10 * 60 * 1)):
                            cancelled = self.cancelBuy()
                            if cancelled == 0:
                                self.coin.boughtTime = ''
                                self.coin.lastBuyOrderID = ''
                                self.coin.numBought = 0.00
                                self.coin.purchasedPrice = 0.00
                                self.coin.numHeld = self.coin.numHeld - self.coin.numBought
                                self.boughtIn = False
                        print("Buy not yet completed")
                if self.coin.lastSellOrderID != '' and self.boughtIn == True:
                    if(self.sellComplete()):
                        print("Sale Completed")
                        self.boughtIn = False

                if last_rsi > self.rsiOverbought:
                    if self.boughtIn:
                        self.sell()
                    else:
                        print("Nothing to sell")
                
                if last_rsi < self.rsiOversold:
                    if self.boughtIn:
                        print("Already in Position")
                    else:
                        self.buy()

            signal.signal(signal.SIGINT, self.killBot)
            time.sleep(15)

def main():
    b = bot()
    b.runBot()

if __name__ == "__main__":
    main()