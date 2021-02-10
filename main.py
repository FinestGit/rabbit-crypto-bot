import rsiBot

def main():
    r = rsiBot.rsiBot()
    print(r.getRSI())
    print(r.getLastRSI())
    print(r.getRSIWindow())
    print(r.getRSIOverbought())
    print(r.getRSIOversold())
    print(r.getDataTrend())

if __name__ == "__main__":
    main()