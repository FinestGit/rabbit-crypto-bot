import robin_stocks as r

class dataBot:
    # Eventually we want an enum for taking care of interval, span, bounds, and info
    def getHistoricalData(self, symbol):
        try:
            historicalData = r.get_crypto_historicals(symbol=symbol, interval='15second', span='hour', bounds='24_7', info='close_price')
            return historicalData
        except:
            print("Data Bot: Could not retrieval historical data for {}".format(symbol))