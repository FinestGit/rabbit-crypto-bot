import sys
import config as cfg
import rsiBot
import signal
import time

class conductorBot:
    def __init__(self):
        print("Conductor Bot: I shall conduct")
        self.__rsiBot = rsiBot.rsiBot()
        self.loadConfig()
    
    def loadConfig(self):
        print("\nConductor Bot: Loading config...")
        print("Conductor Bot: Loading RSI Bot")
        self.__rsiBot.setRSIOverbought(cfg.rsiConfig['rsiOverbought'])
        self.__rsiBot.setRSIOversold(cfg.rsiConfig['rsiOversold'])
        self.__rsiBot.setRSIWindow(cfg.rsiConfig['rsiWindow'])
    
    def killConductor(self, sig, frame):
        print("\nConductor Bot: Shutting down gracefully")
        sys.exit(0)
    
    def orchestrate(self):
        while True:
            print("Orchestrating")
            signal.signal(signal.SIGINT, self.killConductor)
            time.sleep(1)
