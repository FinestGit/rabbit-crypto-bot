import talib
import numpy

class macdBot:
    def __init__(self):
        self.__macd = None
        self.__macdSignal = None
        self.__macdHistogram = None
        self.__lastMacd = None
        self.__lastMacdSignal = None
        self.__checkedHistogram = None
        self.__checkedHistogramWindow = 0
        self.__dataTrend = []
    
    def getMACD(self):
        if self.__macd == None:
            print("MACD Bot: No MACD is available")
            return
        return self.__macd
    
    def getMACDSignal(self):
        if self.__macdSignal == None:
            print("MACD Bot: No MACD Signal is available")
            return
        return self.__macdSignal
        
    def getMACDHistogram(self):
        if self.__macdHistogram == None:
            print("MACD Bot: No MACD Histogram is available")
            return
        return self.__macdHistogram
    
    def getLastMACD(self):
        if self.__lastMacd == None:
            print("MACD Bot: No Last MACD is available")
            return
        return self.__lastMacd
    
    def getLastMACDSignal(self):
        if self.__lastMacdSignal == None:
            print("MACD Bot: No Last MACD Signal is available")
            return
        return self.__lastMacdSigna
    
    def getCheckedHistogram(self):
        if self.__checkedHistogram == None:
            print("MACD Bot: No Checked Histogram is available")
            return
        return self.__checkedHistogram
    
    def getCheckedHistogramWindow(self):
        if self.__checkedHistogramWindow <= 0:
            print("MACD Bot: No Checked Histogram Window is available")
            return
        return self.__checkedHistogramWindow
    
    def getDataTrend(self):
        if len(self.__dataTrend) <= 0:
            print("MACD Bot: No Data Trend is available")
            return
        return self.__dataTrend