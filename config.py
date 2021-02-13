from dotenv import load_dotenv
import os

load_dotenv()

rh = {
    'username': os.getenv("USERNAME"),
    'password': os.getenv("PASSWORD"),
    'expiration': os.getenv("EXPIRATION"),
}

rsiConfig = {
    'rsiWindow': os.getenv("RSI_WINDOW"),
    'rsiOverbought': os.getenv("RSI_OVERBOUGHT"),
    'rsiOversold': os.getenv("RSI_OVERSOLD"),
}

macdConfig = {
    'checkedHistogramWindow': os.getenv("CHECKED_HISTOGRAM_WINDOW"),
}