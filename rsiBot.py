import talib
import numpy

class rsiBot:

    def __init__(self):
        self._rsi = None
        self._lastRsi = None
        self._rsiWindow = 0
        self._rsiOverbought = 0
        self._rsiOversold = 0
        self._dataTrend = []
    
    def getRSI(self):
        if self._rsi == None:
            print("No RSI is available")
            return None
        return self._rsi
    
    def getLastRSI(self):
        if self._lastRsi == None:
            print("No Last RSI is available")
            return None
    
    def getRSIWindow(self):
        if self._rsiWindow <= 0:
            print("No RSI Window available")
            return 0
        return self._rsiWindow
    
    def getRSIOverbought(self):
        if self._rsiOverbought <= 0:
            print("No RSI Overbought available")
            return 0
        return self._rsiOverbought
    
    def getRSIOversold(self):
        if self._rsiOversold <= 0:
            print("No RSI Oversold available")
            return 0
        return self._rsiOversold
    
    def getDataTrend(self):
        if len(self._dataTrend) <= 0:
            print("No Data Trend is available")
            return []
        return self._dataTrend
    
    def setRSIWindow(self, rsiWindow):
        if rsiWindow <= 0:
            print("Cannot set RSI Window to anything less than 1")
            return
        self._rsiWindow = rsiWindow
    
    def setRSIOverbought(self, rsiOverbought):
        if rsiOverbought <= 0:
            print("Cannot set RSI Overbought to a value less than 1")
        if self._rsiOversold > 0 and rsiOverbought < self._rsiOversold:
            print("Cannot set RSI Overbought to a value less than RSI Oversold")
        self._rsiOverbought = rsiOverbought
    
    def setRSIOversold(self, rsiOversold):
        if rsiOversold <= 0:
            print("Cannot set RSI Oversold to a value less than 1")
        if self._rsiOverbought > 0 and rsiOversold > self._rsiOverbought:
            print("Cannot set RSI Oversold to a value greater than RSI Overbought")
        self._rsiOversold = rsiOversold
    
    def addToDataTrend(self, value):
        try:
            f_value = float(value)
            self._dataTrend.append(f_value)
        except ValueError:
            print("Unable to convert value to float, cannot add to Data Trend")
            return
    
    def calculateRSI(self):
        if self._rsiWindow <= 0:
            print("Unable to calculate RSI, RSI Window is too low")
            return
        if len(self._dataTrend) <= 0:
            print("Unable to calculate RSI, Data Trend too small")
        if len(self._dataTrend) < self._rsiWindow:
            print("Unable to calculate RSI, Data Trend small then RSI Window")
        np_dataTrend = numpy.array(self._dataTrend)
        self._rsi = talib.RSI(np_dataTrend, self._rsiWindow)
    
    def trainRSIBot(self, trainingData):
        if len(trainingData) <= 0:
            print("No Training Data provided")
            return
        for data in trainingData:
            self.addToDataTrend(data)