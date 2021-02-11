import talib
import numpy

class rsiBot:

    def __init__(self):
        self.__rsi = None
        self.__lastRsi = None
        self.__rsiWindow = 0
        self.__rsiOverbought = 0
        self.__rsiOversold = 0
        self.__dataTrend = []
    
    def getRSI(self):
        if self.__rsi == None:
            print("RSI Bot: No RSI is available")
            return None
        return self.__rsi
    
    def getLastRSI(self):
        if self.__lastRsi == None:
            print("RSI Bot: No Last RSI is available")
            return None
    
    def getRSIWindow(self):
        if self.__rsiWindow <= 0:
            print("RSI Bot: No RSI Window available")
            return 0
        return self.__rsiWindow
    
    def getRSIOverbought(self):
        if self.__rsiOverbought <= 0:
            print("RSI Bot: No RSI Overbought available")
            return 0
        return self.__rsiOverbought
    
    def getRSIOversold(self):
        if self.__rsiOversold <= 0:
            print("RSI Bot: No RSI Oversold available")
            return 0
        return self.__rsiOversold
    
    def getDataTrend(self):
        if len(self.__dataTrend) <= 0:
            print("RSI Bot: No Data Trend is available")
            return []
        return self.__dataTrend
    
    def setRSIWindow(self, rsiWindow):
        if rsiWindow <= 0:
            print("RSI Bot: Cannot set RSI Window to anything less than 1")
            return
        self.__rsiWindow = rsiWindow
    
    def setRSIOverbought(self, rsiOverbought):
        if rsiOverbought <= 0:
            print("RSI Bot: Cannot set RSI Overbought to a value less than 1")
        if self.__rsiOversold > 0 and rsiOverbought < self.__rsiOversold:
            print("RSI Bot: Cannot set RSI Overbought to a value less than RSI Oversold")
        self.__rsiOverbought = rsiOverbought
    
    def setRSIOversold(self, rsiOversold):
        if rsiOversold <= 0:
            print("RSI Bot: Cannot set RSI Oversold to a value less than 1")
        if self.__rsiOverbought > 0 and rsiOversold > self.__rsiOverbought:
            print("RSI Bot: Cannot set RSI Oversold to a value greater than RSI Overbought")
        self.__rsiOversold = rsiOversold
    
    def addToDataTrend(self, value):
        try:
            f_value = float(value)
            self.__dataTrend.append(f_value)
        except ValueError:
            print("RSI Bot: Unable to convert value to float, cannot add to Data Trend")
            return
    
    def calculateRSI(self):
        if self.__rsiWindow <= 0:
            print("RSI Bot: Unable to calculate RSI, RSI Window is too low")
            return
        if len(self.__dataTrend) <= 0:
            print("RSI Bot: Unable to calculate RSI, Data Trend too small")
        if len(self.__dataTrend) < self.__rsiWindow:
            print("RSI Bot: Unable to calculate RSI, Data Trend small then RSI Window")
        np_dataTrend = numpy.array(self.__dataTrend)
        self.__rsi = talib.RSI(np_dataTrend, self.__rsiWindow)
    
    def trainRSIBot(self, trainingData):
        if len(trainingData) <= 0:
            print("RSI Bot: No Training Data provided")
            return
        for data in trainingData:
            self.addToDataTrend(data)