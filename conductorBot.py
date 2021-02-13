import sys
import signal
import time

# Bot imports
import rsiBot
import macdBot
import sessionBot

# Config imports
import config as cfg

class conductorBot:
    def __init__(self):
        print("Conductor Bot: I shall conduct")
        self.__rsiBot = rsiBot.rsiBot()
        self.__macdBot = macdBot.macdBot()
        self.__sessionBot = sessionBot.sessionBot()
        self.loadConfig()
    
    def loadConfig(self):
        print("\nConductor Bot: Loading config...")

        # RSI Bot configuration occurs here
        print("Conductor Bot: Loading RSI Bot")
        self.__rsiBot.setRSIOverbought(cfg.rsiConfig['rsiOverbought'])
        self.__rsiBot.setRSIOversold(cfg.rsiConfig['rsiOversold'])
        self.__rsiBot.setRSIWindow(cfg.rsiConfig['rsiWindow'])

        # MACD Bot configuration occurs here
        print("Conductor Bot: Loading MACD Bot")
        self.__macdBot.setCheckedHistogramWindow(cfg.macdConfig['checkedHistogramWindow'])

        # Session Bot configuration occurs here
        print("Conductor Bot: Loading Session Bot")
        self.__sessionBot.setUsername(cfg.rh['username'])
        self.__sessionBot.setPassword(cfg.rh['password'])
        self.__sessionBot.setSessionLength(cfg.rh['expiration'])
        self.__sessionBot.sessionStart()

        # Cash Bot configuration occurs here

        # Quote Bot configuration occurs here

        # Buy Bot configuration occurs here

        # Sell Bot configuration occurs here
    
    def killConductor(self, sig, frame):
        print("\nConductor Bot: Shutting down gracefully")
        self.__sessionBot.sessionEnd()
        sys.exit(0)
    
    def orchestrate(self):
        while True:
            print("Orchestrating")
            signal.signal(signal.SIGINT, self.killConductor)
            time.sleep(1)
