# scanner.py - Fixed version matching your setup
import requests
import pandas as pd
from datetime import datetime

def scan_gaps():
    try:
        # Get FTSE 100 tickers
        ftse = pd.read_html('https://en.wikipedia.org/wiki/FTSE_100_Index')[4]
        tickers = [t + '.L' for t in ftse['Ticker'].tolist()][:10]  # Top 10
        
        alerts = []
        for t in tickers:
            try:
                # Get price data
                url = f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?interval=1m&range=2d"
                data = requests.get(url).json()['chart']['result'][0]
                prev_close = data['meta']['previousClose']
                curr_price = data['indicators']['quote'][0]['open'][-1]
                volume = data['indicators']['quote'][0]['volume'][-1]
                
                # Check gap
                gap_pct = (curr_price - prev_close) / prev_close * 100
                if abs(gap_pct) > 2.0 and volume > 1000000:
                    alerts.append({
                        'ticker': t,
                        'gap_pct': round(gap_pct, 2),
                        'time': datetime.now().strftime("%H:%M:%S"),
                        'entry_price': curr_price
                    })
            except:
                continue
        return alerts
    except Exception as e:
        print(f"Scanner error: {e}")
        return []

if __name__ == "__main__":
    print(scan_gaps())
