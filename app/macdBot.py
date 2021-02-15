import talib
import numpy

class macdBot:
    def __init__(self):
        self.__macdState = {}
        self.__checkedHistogramWindow = 0

    def getMACDState(self):
        if not self.__macdState:
            print("MACD Bot: No MACD States are available")
            return {}
        return self.__macdState
    
    def getMACDStateForSymbol(self, symbol):
        if symbol == '':
            print("MACD Bot: Cannot get MACD State for empty string")
            return None
        if symbol not in self.__macdState:
            print("MACD Bot: MACD State is not available for {}".format(symbol))
            return None
        macdState = self.__macdState[symbol]
        if not macdState:
            print("MACD Bot: MACD State is not available for {}".format(symbol))
            return None
        return macdState
    
    def getMACDForSymbol(self, symbol):
        macdState = self.getMACDStateForSymbol(symbol)
        if macdState == None:
            print("MACD Bot: MACD is not available for {}".format(symbol))
            return []
        macd = macdState['macd']
        if len(macd) <= 0:
            print("MACD Bot: MACD is not available for {}".format(symbol))
            return []
        return macd
    
    def getMACDSignalForSymbol(self, symbol):
        macdState = self.getMACDStateForSymbol(symbol)
        if macdState == None:
            print("MACD Bot: MACD Signal is not available for {}".format(symbol))
            return []
        macdSignal = macdState['macdSignal']
        if len(macdSignal) <= 0:
            print("MACD Bot: MACD Signal is not available for {}".format(symbol))
            return []
        return macdSignal
        
    def getMACDHistogramForSymbol(self, symbol):
        macdState = self.getMACDStateForSymbol(symbol)
        if macdState == None:
            print("MACD Bot: MACD Histogram is not available for {}".format(symbol))
            return []
        macdHistogram = macdState['macdHistogram']
        if len(macdHistogram) <= 0:
            print("MACD Bot: MACD Histogram is not available for {}".format(symbol))
            return []
        return macdHistogram
    
    def getLastMACDForSymbol(self, symbol):
        macdState = self.getMACDStateForSymbol(symbol)
        if macdState == None:
            print("MACD Bot: Last MACD is not available for {}".format(symbol))
            return None
        lastMacd = macdState['lastMacd']
        return lastMacd
    
    def getLastMACDSignalForSymbol(self, symbol):
        macdState = self.getMACDStateForSymbol(symbol)
        if macdState == None:
            print("MACD Bot: Last MACD Signal is not available for {}".format(symbol))
            return None
        lastMacdSignal = macdState['lastMacdSignal']
        return lastMacdSignal
    
    def getCheckedHistogramForSymbol(self, symbol):
        macdState = self.getMACDStateForSymbol(symbol)
        if macdState == None:
            print("MACD Bot: Checked MACD Histogram is not available for {}".format(symbol))
            return []
        checkedHistogram = macdState['checkedHistogram']
        if len(checkedHistogram) <= 0:
            print("MACD Bot: MACD Signal is not available for {}".format(symbol))
            return []
        return checkedHistogram
    
    def getCheckedHistogramWindow(self):
        if self.__checkedHistogramWindow <= 0:
            print("MACD Bot: No Checked Histogram Window is available")
            return 0
        return self.__checkedHistogramWindow
    
    def getDataTrendForSymbol(self, symbol):
        macdState = self.getMACDStateForSymbol(symbol)
        if macdState == None:
            print("MACD Bot: Data Trend is not available for {}".format(symbol))
            return []
        dataTrend = macdState['dataTrend']
        if len(dataTrend) <= 0:
            print("MACD Bot: Data Trend is not available for {}".format(symbol))
            return []
        return dataTrend
    
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
    
    def addToDataTrendForSymbol(self, symbol, value):
        try:
            f_value = float(value)
            macdState = self.getMACDStateForSymbol(symbol)
            if macdState == None:
                print("MACD Bot: Data Trend is not available for {}".format(symbol))
                return
            dataTrend = macdState['dataTrend']
            dataTrend.append(f_value)
        except ValueError:
            print("MACD Bot: Unable to convert value to float, cannot add to Data Trend for {}".format(symbol))
            return
    
    def calculatedMACDForSymbol(self, symbol):
        if self.__checkedHistogramWindow <= 0:
            print("MACD Bot: Unable to calculate MACD for {}, Checked Histogram Window too low".format(symbol))
            return
        macdState = self.getMACDStateForSymbol(symbol)
        dataTrend = macdState['dataTrend']
        if len(dataTrend) <= 0:
            print("MACD Bot: Unable to calculate MACD for {}, Data Trend too small".format(symbol))
            return
        if len(dataTrend) <= 26:
            print("MACD Bot: Unable to calculate MACD for {}, Data Trend must have 26 entries".format(symbol))
        np_datatrend = numpy.array(dataTrend)
        macd = macdState['macd']
        macdSignal = macdState['macdSignal']
        macdHistogram = macdState['macdHistogram']
        macd, macdSignal, macdHistogram = talib.MACD(np_datatrend)
        macdState['lastMacd'] = macd[-1]
        macdState['lastMacdSignal'] = macdSignal[-1]
        macdState['checkedHistogram'] = macdHistogram[(-(self.__checkedHistogramWindow))]
    
    def trainMACDBotForSymbol(self, symbol, trainingData):
        if len(trainingData) <= 0:
            print("MACD Bot: No Training Data provided")
            return
        for data in trainingData:
            self.addToDataTrendForSymbol(symbol, data)
        self.calculatedMACDForSymbol(symbol)
    
    def addMACD(self, symbol):
        new_MACD = {
            symbol: {
                'macd': [],
                'macdSignal': [],
                'macdHistogram': [],
                'lastMacd': 0,
                'lastMacdSignal': 0,
                'checkedHistogram': [],
                'dataTrend': []
            }
        }
        self.__macdState.update(new_MACD)