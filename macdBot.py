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
            return None
        return self.__macd
    
    def getMACDSignal(self):
        if self.__macdSignal == None:
            print("MACD Bot: No MACD Signal is available")
            return None
        return self.__macdSignal
        
    def getMACDHistogram(self):
        if self.__macdHistogram == None:
            print("MACD Bot: No MACD Histogram is available")
            return None
        return self.__macdHistogram
    
    def getLastMACD(self):
        if self.__lastMacd == None:
            print("MACD Bot: No Last MACD is available")
            return None
        return self.__lastMacd
    
    def getLastMACDSignal(self):
        if self.__lastMacdSignal == None:
            print("MACD Bot: No Last MACD Signal is available")
            return None
        return self.__lastMacdSigna
    
    def getCheckedHistogram(self):
        if self.__checkedHistogram == None:
            print("MACD Bot: No Checked Histogram is available")
            return None
        return self.__checkedHistogram
    
    def getCheckedHistogramWindow(self):
        if self.__checkedHistogramWindow <= 0:
            print("MACD Bot: No Checked Histogram Window is available")
            return 0
        return self.__checkedHistogramWindow
    
    def getDataTrend(self):
        if len(self.__dataTrend) <= 0:
            print("MACD Bot: No Data Trend is available")
            return []
        return self.__dataTrend
    
    def setCheckedHistogramWindow(self, checkedHistogramWindow):
        try:
            i_checkedHistogramWindow = int(checkedHistogramWindow)
        except ValueError:
            print("MACD Bot: Could not assign Checked Histogram Window to a value that is not an int")
            return
        if i_checkedHistogramWindow <= 0:
            print("MACD Bot: Cannot set Checked Histogram Window to any value less than 1")
            return
        self.__checkedHistogramWindow = i_checkedHistogramWindow
        
    
    def addToDataTrend(self, value):
        try:
            f_value = float(value)
            self.__dataTrend.append(f_value)
        except ValueError:
            print("MACD Bot: Unable to convert value to float, cannot add to data trend")
            return
    
    def calculatedMACD(self):
        if self.__checkedHistogramWindow <= 0:
            print("MACD Bot: Unable to calculate MACD, Checked Histogram Window too low")
            return
        if len(self.__dataTrend) <= 0:
            print("MACD Bot: Unable to calculate MACD, Data Trend too small")
        if len(self.__dataTrend) <= 26:
            print("MACD Bot: Unable to calculate MACD, Data Trend must have 26 entries")
        np_datatrend = numpy.array(self.__dataTrend)
        self.__macd, self.__macdSignal, self.__macdHistogram = talib.MACD(np_datatrend)
        self.__lastMacd = self.__macd[-1]
        self.__lastMacdSignal = self.__macd[-1]
        self.__checkedHistogram = self.__macdHistogram[(-(self.__checkedHistogramWindow))]
    
    def trainMACDBot(self, trainingData):
        if len(trainingData) <= 0:
            print("MACD Bot: No Training Data provided")
            return
        for data in trainingData:
            self.addToDataTrend(data)
        self.calculatedMACD()
