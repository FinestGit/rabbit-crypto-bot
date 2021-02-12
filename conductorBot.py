import sys
import signal
import time
import config as cfg
import rsiBot
import sessionBot

class conductorBot:
    def __init__(self):
        print("Conductor Bot: I shall conduct")
        self.__rsiBot = rsiBot.rsiBot()
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
        print("Condcutor Bot: Loading MACD Bot")

        # Session bot configuration occurs here
        print("Conductor Bot: Loading Session Bot")
        self.__sessionBot.setUsername(cfg.rh['username'])
        self.__sessionBot.setPassword(cfg.rh['password'])
        self.__sessionBot.setSessionLength(cfg.rh['expiration'])
        self.__sessionBot.sessionStart()
    
    def killConductor(self, sig, frame):
        print("\nConductor Bot: Shutting down gracefully")
        self.__sessionBot.sessionEnd()
        sys.exit(0)
    
    def orchestrate(self):
        while True:
            print("Orchestrating")
            signal.signal(signal.SIGINT, self.killConductor)
            time.sleep(1)
