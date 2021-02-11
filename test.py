import time
import testingConfig as cfg
import robin_stocks as r
import talib
import numpy
import sys
import signal
import math
import datetime

class coin:
    purchasedPrice = 0.0
    numBought = 0.0
    name = ""
    lastBuyOrderID = ""
    lastSellOrderID = ""
    boughtTime = ""
    sellPrice = 0.00

    def __init__(self, name=""):
        self.name = name
        self.purchasedPrice = 0.0
        self.numBought = 0.0
        self.lastBuyOrderID = ""
        self.lastSellOrderID = ""
        self.boughtTime = ""
        self.sellPrice = 0.0

class bot:
    tradesEnabled = False
    rsiWindow = 0
    boughtIn = False
    rsiOverbought = 0
    rsiOversold = 0
    minCoinIncrement = 0.00
    minPriceIncrement = 0.00
    minOrderSize = 0.00
    profit = 0.00
    marketType = ''
    buyPrices = []
    sellPrices = []
    coinTrend = []

    def __init__(self):
        self.loadConfig()

        Result = r.login(self.rh_user, self.rh_pw, 86400, by_sms=True)

        self.train()
    
    def loadConfig(self):
        print("\nLoading Config...")
        self.rsiWindow = cfg.RSI_PERIOD
        self.rsiOverboughtUpper = 80
        self.rsiOverboughtLower = cfg.RSI_OVERBOUGHT
        self.rsiOversoldUpper = cfg.RSI_OVERSOLD
        self.rsiOversoldLower = 20
        self.rh_user = cfg.USERNAME
        self.rh_pw = cfg.PASSWORD
        self.coin = coin(cfg.TRADE_SYMBOL)
        print("\n")
    
    def getCurrentPrice(self):
        try:
            result = r.get_crypto_quote(self.coin.name)
            price = self.roundDown(float(result['mark_price']), self.minPriceIncrement)
        except:
            print("Problem retrieving crypto quote")
            return 0
        return float(price)
    
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
        # to disable checking profitability uncomment this
        # return True
        price = float(self.getCurrentPrice())
        total_sale = float(self.coin.numBought * price)
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
    
    def getProfits(self):
        i = 0
        if len(self.buyPrices) == len(self.sellPrices):
            for buyPrice in self.buyPrices:
                self.profit += self.sellPrices[i] - buyPrice
                i += 1
        else:
            print("Something went wrong between buy and sell prices")
            print(self.buyPrices)
            print(self.sellPrices)

    def buyComplete(self):
        try:
            result = r.get_crypto_order_info(self.coin.lastBuyOrderID)
            state = result['state']
            if state == 'filled':
                cost = self.roundDown((float(result['price']) * float(result['quantity'])), 0.01)
                self.buyPrices.append(cost)
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
                cost = self.roundDown((float(result['price']) * float(result['quantity'])), 0.01)
                self.sellPrices.append(cost)
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
        print("In Buy")
        availableCash = float(self.getCash())
        if availableCash == -1:
            print("Got an exception checking for available cash, cancelling buy.")
            return
        else:
            if self.tradesEnabled == True:
                try:
                    price = self.roundDown(self.getCurrentPrice(), self.minPriceIncrement)
                    buyable_qty = self.roundDown(self.getBuyingPower(availableCash, price), self.minCoinIncrement)
                    if buyable_qty > 0:
                        try:
                            print("Buying")
                            result = r.order_buy_crypto_limit(self.coin.name, buyable_qty, price)
                            self.coin.purchasedPrice = price
                            self.coin.numBought = buyable_qty
                            print(result)
                            self.coin.lastBuyOrderID = result['id']
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
        print("In Sell")
        if self.coin.numBought <= 0:
            print("No coins to sell")
            return
        if self.tradesEnabled == True:
            if self.getProfitability():
                price = self.roundDown(self.getCurrentPrice(), self.minPriceIncrement)
                sellable_qty = self.roundDown(self.coin.numBought, self.minCoinIncrement)
                if sellable_qty > 0:
                    try:
                        print("Selling")
                        result = r.order_sell_crypto_limit(self.coin.name, sellable_qty, price)
                        self.coin.purchasedPrice = 0.0
                        self.coin.sellPrice = price
                        self.coin.numBought = 0.0
                        self.coin.lastBuyOrderID = ''
                        self.coin.boughtTime = ''
                        print(result)
                        self.coin.lastSellOrderID = result['id']
                    except:
                        print("Error selling, cancelling sale.")
                        return
            else:
                print("Not Profitable Holding")
        return
    
    def macdCheck(self, macd, macdSignal, macdHist):
        checkedHist = macdHist[-7:]
        if macd[-1] > macdSignal[-1]:
            count = 0
            for hist in checkedHist:
                if hist < 0:
                    count += 1
            if count < 5:
                return
            self.marketType = "Bullish"
            self.rsiOverboughtUpper = 90
            self.rsiOverboughtLower = 80
            self.rsiOversoldUpper = 50
            self.rsiOversoldLower = 40
        if macd[-1] < macdSignal[-1]:
            count = 0
            for hist in checkedHist:
                if hist > 0:
                    count += 1
            if count < 5:
                return
            self.marketType = "Bearish"
            self.rsiOverboughtUpper = 65
            self.rsiOverboughtLower = 55
            self.rsiOversoldUpper = 30
            self.rsiOversoldLower = 20
    
    def train(self):
        self.tradesEnabled = False
        try:
            training_data = r.get_crypto_historicals(symbol=self.coin.name, interval='15second', span='hour', bounds='24_7', info='close_price')
            for data in training_data:
                self.coinTrend.append(float(data))
                np_closes = numpy.array(self.coinTrend)
                rsi = talib.RSI(np_closes, self.rsiWindow)
                last_rsi = rsi[-1]
                macd, macdsignal, macdhist = talib.MACD(np_closes)
                self.macdCheck(macd, macdsignal, macdhist)
                print("Current rsi {}".format(last_rsi))
                self.tradesEnabled = cfg.TRADING_ENABLED
        except:
            print("Problem fetching training data")
            return
    
    def killBot(self, sig, frame):
        print('Exiting...')
        print(self.buyPrices)
        print(self.sellPrices)
        self.getProfits()
        print(self.profit)
        r.logout()
        sys.exit(0)
    
    def roundDown(self, x, a):
        return math.floor(x/a) * a
    
    def runBot(self):
        self.getIncrements()

        while True:
            current_price = self.getCurrentPrice()
            if current_price > 0:
                self.coinTrend.append(self.getCurrentPrice())
            else:
                self.coinTrend.append(self.coinTrend[-1])
            
            now = datetime.datetime.now()

            if len(self.coinTrend) > self.rsiWindow:
                np_closes = numpy.array(self.coinTrend)
                rsi = talib.RSI(np_closes, self.rsiWindow)
                last_rsi = rsi[-1]
                macd, macdsignal, macdhist = talib.MACD(np_closes)
                self.macdCheck(macd, macdsignal, macdhist)
                print(self.marketType)
                print("Current rsi {}".format(last_rsi))

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
                                self.boughtIn = False
                        print("Buy not yet completed")
                if self.coin.lastSellOrderID != '' and self.boughtIn == True:
                    if(self.sellComplete()):
                        print("Sale Completed")
                        print("Sold {} {} @ {}".format(self.coin.numBought, self.coin.name, self.coin.sellPrice))
                        self.coin.lastSellOrderID = ''
                        self.coin.sellPrice = 0.00
                        self.boughtIn = False

                if (last_rsi > self.rsiOverboughtLower) and (last_rsi < self.rsiOverboughtUpper) and (self.coin.lastSellOrderID == ''):
                    if self.boughtIn:
                        self.sell()
                    else:
                        print("Nothing to sell")
                
                if (last_rsi < self.rsiOversoldUpper) and (last_rsi > self.rsiOversoldLower) and (self.coin.lastBuyOrderID == ''):
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