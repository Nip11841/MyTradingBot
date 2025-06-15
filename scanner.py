# From the GitHub structure - with configurable thresholds and error handling
import yfinance as yf
import pandas as pd
import json
from datetime import datetime

with open('config.json') as f:
    config = json.load(f)

def scan_gaps():
    ftse = pd.read_html(config['ticker_list_url'])[4]
    tickers = [t + '.L' for t in ftse['Ticker'].tolist()][:config['max_tickers']]
    
    alerts = []
    for t in tickers:
        try:
            data = yf.download(t, period='2d', interval='1m', prepost=True)
            if len(data) > 30:
                prev_close = data['Close'].iloc[-2]
                curr_open = data['Open'].iloc[-1]
                gap_pct = (curr_open - prev_close) / prev_close * 100
                
                if (abs(gap_pct) > config['gap_threshold'] and 
                    data['Volume'].iloc[-1] > config['min_volume']):
                    alerts.append({
                        'ticker': t,
                        'gap_pct': round(gap_pct, 2),
                        'time': datetime.now().strftime("%H:%M")
                    })
        except Exception as e:
            print(f"Error with {t}: {str(e)}")
    
    return alerts
