# gap_volume_scanner.py - Free Pre-Market Gap Detector
import yfinance as yf
import pandas as pd

def scan_gaps():
    # Step 1: Get FTSE 100 tickers (free Yahoo list)
    ftse = pd.read_html('https://en.wikipedia.org/wiki/FTSE_100_Index')[4]
    tickers = [t + '.L' for t in ftse['Ticker'].tolist()][:10]  # Top 10 only
    
    # Step 2: Check pre-market gaps and volume
    gaps = []
    for t in tickers:
        data = yf.download(t, period='2d', interval='1m', prepost=True)
        if len(data) > 30:  # Has pre-market data
            prev_close = data['Close'].iloc[-2]
            curr_open = data['Open'].iloc[-1]
            gap_pct = (curr_open - prev_close) / prev_close * 100
            
            if abs(gap_pct) > 2 and data['Volume'].iloc[-1] > 1000000:
                gaps.append((t, gap_pct))
    
    # Step 3: Generate alerts
    if gaps:
        print("TRADE THESE AT OPEN:")
        for t, gap in sorted(gaps, key=lambda x: abs(x[1]), reverse=True):
            print(f"{t}: {'UP' if gap >0 else 'DOWN'} {abs(gap):.1f}%")
    else:
        print("No qualified gaps today")

scan_gaps()
