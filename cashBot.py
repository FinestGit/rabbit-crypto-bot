import robin_stocks as r

class cashBot:
    def __init__(self):
        self.__cashOnHand = 0
        self.__maximumUsableCash = 0
    
    def getCashOnHand(self):
        if self.__cashOnHand <= 0:
            print("Cash Bot: No Cash On Hand is available")
            return 0
        return self.__cashOnHand
    
    def getMaximumUsableCash(self):
        if self.__maximumUsableCash <= 0:
            print("Cash Bot: No Maximum Usable Cash is available")
            return 0
        return self.__maximumUsableCash
    
    def setMaximumUsableCash(self, maximumCash):
        try:
            i_maximumCash = int(maximumCash)
        except ValueError:
            print("Cash Bot: Cannot set Maximum Usable Cash to a value that is not an int")
        if i_maximumCash <= 0:
            print("Cash Bot: Cannot set Maximum Usable Cash to a value less than 1")
            return
        self.__maximumUsableCash = i_maximumCash
    
    def getRobinhoodCash(self):
        try:
            account = r.load_account_profile()
            print(account)
        except:
            print("Issue retrieving Cash On Hand from Robinhood")
            return -1.0