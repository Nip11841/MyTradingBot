# Runs every 5 mins to monitor open trades
import yfinance as yf
import time

def check_stops(ticker, entry_px, stop_pct):
    while True:
        current = yf.Ticker(ticker).history(period='1d')['Close'].iloc[-1]
        if current <= entry_px * (1 - stop_pct/100):
            print(f"STOP HIT: {ticker} at {current}")
            break
        time.sleep(300)  # Check every 5 mins
