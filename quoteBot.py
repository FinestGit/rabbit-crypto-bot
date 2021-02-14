import datetime

import robin_stocks as r

class quoteBot:
    def __init__(self):
        self.__quoteState = {}
    
    def getCurrentQuoteState(self):
        if not self.__quoteState:
            print("Quote Bot: No Quote States are available")
            return {}
        return self.__quoteState
    
    def getSymbolQuote(self, symbol):
        for quote in self.__quoteState:
            if quote == symbol:
                return self.__quoteState[quote]
        print("Quote Bot: No Quote was found for the symbol {}".format(symbol))
    
    def getAskPrice(self, symbol):
        quote = self.getSymbolQuote(symbol)
        askPrice = quote['ask_price']
        if askPrice <= 0:
            print("Quote Bot: No Ask Price found for the symbol {}".format(symbol))
            return -1
        return askPrice   

    def getBidPrice(self, symbol):
        quote = self.getSymbolQuote(symbol)
        bidPrice = quote['bid_price']
        if bidPrice <= 0:
            print("Quote Bot: No Bid Price found for the symbol {}".format(symbol))
            return -1
        return bidPrice

    def getMarkPrice(self, symbol):
        quote = self.getSymbolQuote(symbol)
        markPrice = quote['mark_price']
        if markPrice <= 0:
            print("Quote Bot: No Mark Price found for the symbol {}".format(symbol))
            return -1
        return markPrice

    def getHighPrice(self, symbol):
        quote = self.getSymbolQuote(symbol)
        highPrice = quote['high_price']
        if highPrice <= 0:
            print("Quote Bot: No High Price found for the symbol {}".format(symbol))
            return -1
        return highPrice

    def getLowPrice(self, symbol):
        quote = self.getSymbolQuote(symbol)
        lowPrice = quote['low_price']
        if lowPrice <= 0:
            print("Quote Bot: No Low Price found for the symbol {}".format(symbol))
            return -1
        return lowPrice

    def getOpenPrice(self, symbol):
        quote = self.getSymbolQuote(symbol)
        openPrice = quote['open_price']
        if openPrice <= 0:
            print("Quote Bot: No Open Price found for the symbol {}".format(symbol))
            return -1
        return openPrice

    def addQuote(self, symbol):
        now = datetime.datetime.now()
        try:
            result = r.get_crypto_quote(symbol)
            new_quote = {
                symbol: {
                    'askPrice': result['ask_price'],
                    'bidPrice': result['bid_price'],
                    'markPrice': result['mark_price'],
                    'highPrice': result['high_price'],
                    'lowPrice': result['low_price'],
                    'openPrice': result['open_price'],
                    'quoteUpdateTime': str(now)
                }
            }
            self.__quoteState.update(new_quote)
        except:
            print("Quote Bot: Could not retrieve crypto quote, could not add new quote")
    
    def updateQuotes(self):
        now = datetime.datetime.now()
        for quote in self.__quoteState:
            try:
                result = r.get_crypto_quote(quote)
                updated_quote = {
                    quote: {
                        'askPrice': result['ask_price'],
                        'bidPrice': result['bid_price'],
                        'markPrice': result['mark_price'],
                        'highPrice': result['high_price'],
                        'lowPrice': result['low_price'],
                        'openPrice': result['open_price'],
                        'quoteUpdateTime': str(now)
                    }
                }
                self.__quoteState.update(updated_quote)
            except:
                print("Quote Bot: Could not retrieve crypto quote for {}".format(quote))
                return