import sys
import signal
import time
import os.path as path

# Bot imports
import rsiBot
import macdBot
import sessionBot
import cashBot
import pickleBot
import quoteBot

# Config imports
import config as cfg

class conductorBot:
    def __init__(self):
        print("Conductor Bot: I shall conduct")
        self.__pickleBot = pickleBot.pickleBot()
        self.__rsiBot = rsiBot.rsiBot()
        self.__macdBot = macdBot.macdBot()
        self.__sessionBot = sessionBot.sessionBot()
        self.__cashBot = cashBot.cashBot()
        self.__quoteBot = quoteBot.quoteBot()
        self.loadConfig()
    
    def loadConfig(self):
        print("\nConductor Bot: Loading config...")

        # Session Bot configuration occurs here
        print("Conductor Bot: Loading Session Bot")
        self.__sessionBot.setUsername(cfg.rhConfig['username'])
        self.__sessionBot.setPassword(cfg.rhConfig['password'])
        self.__sessionBot.setSessionLength(cfg.rhConfig['expiration'])
        self.__sessionBot.sessionStart()

        # Pickle Bot configuration occurs here
        print("Conductor Bot: Loading Pickle Bot")
        self.__pickleBot.setPickleFile(cfg.pickleConfig['pickleFile'])
        if path.exists(self.__pickleBot.getPickleFile()):
            print("Conductor Bot: Previous data exists, loading...")
            data = self.__pickleBot.depickle()
            self.__rsiBot = data['rsiBot']
            self.__macdBot = data['macdBot']
            self.__cashBot = data['cashBot']
        
        else:
            # Panda Bot configuration occurs here

            # RSI Bot configuration occurs here
            print("Conductor Bot: Loading RSI Bot")
            self.__rsiBot.setRSIOverbought(cfg.rsiConfig['rsiOverbought'])
            self.__rsiBot.setRSIOversold(cfg.rsiConfig['rsiOversold'])
            self.__rsiBot.setRSIWindow(cfg.rsiConfig['rsiWindow'])

            # MACD Bot configuration occurs here
            print("Conductor Bot: Loading MACD Bot")
            self.__macdBot.setCheckedHistogramWindow(cfg.macdConfig['checkedHistogramWindow'])

            # Cash Bot configuration occurs here
            print("Conductor Bot: Loading Cash Bot")
            self.__cashBot.setMaximumUsableCash(cfg.cashConfig['maximumUsableCash'])
            cash = -1
            while cash < 0:
                cash = self.__cashBot.getRobinhoodCash()
            
            # Quote Bot configuration occurs here
            print("Conductor Bot: Loading Quote Bot")
            for coinSymbol in cfg.quoteConfig['coins']:
                self.__quoteBot.addQuote(coinSymbol)

            # Buy Bot configuration occurs here

            # Sell Bot configuration occurs here

            # Profit Bot configuration occurs here
    
    def combineState(self):
        currentState = {
            "rsiBot": self.__rsiBot,
            "macdBot": self.__macdBot,
            "cashBot": self.__cashBot,
            "quoteBot": self.__quoteBot,
        }
        return currentState
    
    def killConductor(self, sig, frame):
        print("\nConductor Bot: Shutting down gracefully")
        self.__sessionBot.sessionEnd()
        state = self.combineState()
        self.__pickleBot.pickle(state)
        sys.exit(0)
    
    def orchestrate(self):
        while True:
            print("Orchestrating")
            signal.signal(signal.SIGINT, self.killConductor)
            self.__quoteBot.updateQuotes()
            self.__quoteBot.getCurrentQuoteState()

            state = self.combineState()
            self.__pickleBot.pickle(state)
            time.sleep(5)
