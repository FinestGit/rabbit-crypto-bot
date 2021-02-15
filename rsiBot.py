import talib
import numpy

class rsiBot:

    def __init__(self):
        self.__rsiState = {}
        self.__rsiWindow = 0
    
    def getRSIState(self):
        if not self.__rsiState:
            print("RSI Bot: No RSI States are available")
            return {}
        return self.__rsiState
    
    def getRSIStateForSymbol(self, symbol):
        if symbol == '':
            print("RSI Bot: Cannot get RSI State for empty string")
            return None
        if symbol not in self.__rsiState:
            print("RSI Bot: RSI State is not available for {}".format(symbol))
            return None
        rsiState = self.__rsiState[symbol]
        if not rsiState:
            print("RSI Bot: RSI State is not available for {}".format(symbol))
            return None
        return rsiState
    
    def getRSIForSymbol(self, symbol):
        rsiState = self.getRSIStateForSymbol(symbol)
        if rsiState == None:
            print("RSI Bot: RSI is not available for {}".format(symbol))
            return []
        rsi = rsiState['rsi']
        if len(rsi) <= 0:
            print("RSI Bot: RSI is not available for {}".format(symbol))
            return []
        return rsi
    
    def getLastRSIForSymbol(self, symbol):
        rsiState = self.getRSIForSymbol(symbol)
        if rsiState == None:
            print("RSI Bot: Last RSI is not available for {}".format(symbol))
            return -1
        lastRSI = rsiState['lastRsi']
        if lastRSI <= 0:
            print("RSI Bot: Last RSI is not available for {}".format(symbol))
            return -1
        return lastRSI
    
    def getRSIWindow(self):
        if self.__rsiWindow <= 0:
            print("RSI Bot: No RSI Window available")
            return 0
        return self.__rsiWindow
    
    def getRSIOverboughtForSymbol(self, symbol):
        rsiState = self.getRSIForSymbol(symbol)
        if rsiState == None:
            print("RSI Bot: RSI Overbought is not available for {}".format(symbol))
            return -1
        rsiOverbought = rsiState['rsiOverbought']
        if rsiOverbought <= 0:
            print("RSI Bot: RSI Overbought is not available for {}".format(symbol))
            return -1
        return rsiOverbought
    
    def getRSIOversoldForSymbol(self, symbol):
        rsiState = self.getRSIForSymbol(symbol)
        if rsiState == None:
            print("RSI Bot: RSI Oversold is not available for {}".format(symbol))
            return -1
        rsiOversold = rsiState['rsiOversold']
        if rsiOversold <= 0:
            print("RSI Bot: RSI Oversold is not available for {}".format(symbol))
            return -1
        return rsiOversold
    
    def getDataTrendForSymbol(self, symbol):
        rsiState = self.getRSIForSymbol(symbol)
        if rsiState == None:
            print("RSI Bot: Data Trend is not available for {}".format(symbol))
            return []
        dataTrend = rsiState['dataTrend']
        if len(dataTrend) <= 0:
            print("RSI Bot: Data Trend is not available for {}".format(symbol))
            return []
        return dataTrend
    
    def setRSIWindow(self, rsiWindow):
        try:
            i_rsiWindow = int(rsiWindow)
        except ValueError:
            print("RSI Bot: Could not assign RSI Window to a value that is not an int")
            return
        if i_rsiWindow <= 0:
            print("RSI Bot: Cannot set RSI Window to anything less than 1")
            return
        self.__rsiWindow = i_rsiWindow
    
    def setRSIOverboughtForSymbol(self, symbol, rsiOverbought):
        try:
            i_rsiOverbought = int(rsiOverbought)
        except ValueError:
            print("RSI Bot: Could not assign RSI Overbought to a value that is not an int")
            return
        rsiState = self.getRSIStateForSymbol(symbol)
        if rsiState == None:
            print("RSI Bot: RSI Overbought is not available for {}".format(symbol))
            return
        if i_rsiOverbought <= 0:
            print("RSI Bot: Cannot set RSI Overbought for {} to a value less than 1".format(symbol))
            return
        rsiOversold = rsiState['rsiOversold']
        if rsiOversold > 0 and i_rsiOverbought < rsiOversold:
            print("RSI Bot: Cannot set RSI Overbought for {} to a value less than RSI Oversold".format(symbol))
            return
        rsiState['rsiOverbought'] = i_rsiOverbought
 
    def setRSIOversoldForSymbol(self, symbol, rsiOversold):
        try:
            i_rsiOversold = int(rsiOversold)
        except ValueError:
            print("RSI Bot: Could not assign RSI Oversold to a value that is not an int")
            return
        rsiState = self.getRSIStateForSymbol(symbol)
        if rsiState == None:
            print("RSI Bot: RSI Oversold is not available for {}".fromat(symbol))
            return
        if i_rsiOversold <= 0:
            print("RSI Bot: Cannot set RSI Oversold for {} to a value less than 1".format(symbol))
            return
        rsiOverbought = rsiState['rsiOverbought']
        if rsiOverbought > 0 and i_rsiOversold > rsiOverbought:
            print("RSI Bot: Cannot set RSI Oversold for {} to a value greater than RSI Overbought".format(symbol))
            return
        rsiState['rsiOversold'] = i_rsiOversold
    
    def addToDataTrendForSymbol(self, symbol, value):
        try:
            f_value = float(value)
            rsiState = self.getRSIStateForSymbol(symbol)
            if rsiState == None:
                print("RSI Bot: Dat Trend is not available for {}".format(symbol))
                return
            dataTrend = rsiState['dataTrend']
            dataTrend.append(f_value)
        except ValueError:
            print("RSI Bot: Unable to convert value to float, cannot add to Data Trend for {}".format(symbol))
            return
    
    def calculateRSIForSymbol(self, symbol):
        if self.__rsiWindow <= 0:
            print("RSI Bot: Unable to calculate RSI for {}, RSI Window is too low".format(symbol))
            return
        rsiState = self.getRSIStateForSymbol(symbol)
        if len(rsiState['dataTrend']) <= 0:
            print("RSI Bot: Unable to calculate RSI for {}, Data Trend too small".format(symbol))
            return
        if len(rsiState['dataTrend']) < self.__rsiWindow:
            print("RSI Bot: Unable to calculate RSI for {}, Data Trend small then RSI Window".format(symbol))
            return
        np_dataTrend = numpy.array(rsiState['dataTrend'])
        rsiState['rsi'] = talib.RSI(np_dataTrend, self.__rsiWindow)
        rsiState['lastRsi'] = rsiState['rsi'][-1]
        self.__rsiState[symbol].update(rsiState)
    
    def trainRSIBotForSymbol(self, symbol, trainingData):
        if len(trainingData) <= 0:
            print("RSI Bot: No Training Data provided")
            return
        for data in trainingData:
            self.addToDataTrendForSymbol(symbol, data)
        self.calculateRSIForSymbol(symbol)
    
    def addRSI(self, symbol):
        new_RSI = {
            symbol: {
                'rsi': [],
                'lastRsi': 0.00,
                'rsiOverbought': 0,
                'rsiOversold': 0,
                'dataTrend': []
            }
        }
        self.__rsiState.update(new_RSI)