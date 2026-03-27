#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Insider Trading Tracker
Tracks insider buy/sell activity from SEC EDGAR via yfinance
"""

import os
import json
import logging
import pandas as pd
import yfinance as yf
from datetime import datetime
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class InsiderTracker:
    def __init__(self, data_dir: str = './data'):
        self.output_file = os.path.join(data_dir, 'insider_moves.json')
        
    def get_insider_activity(self, ticker: str):
        try:
            stock = yf.Ticker(ticker)
            df = stock.insider_transactions
            if df is None or df.empty:
                return []
            
            # Filter buys in last 6 months
            cutoff = pd.Timestamp.now() - pd.Timedelta(days=180)
            df = df.sort_index(ascending=False)
            
            recent_buys = []
            for date, row in df.iterrows():
                if hasattr(date, 'to_pydatetime') and date < cutoff:
                    continue
                text = str(row.get('Text', '')).lower()
                if 'purchase' not in text and 'buy' not in text:
                    continue
                
                recent_buys.append({
                    'date': str(date.date()) if hasattr(date, 'date') else str(date),
                    'insider': row.get('Insider', 'N/A'),
                    'value': float(row.get('Value', 0) or 0),
                    'shares': int(row.get('Shares', 0) or 0)
                })
            return recent_buys
        except:
            return []

    def analyze_tickers(self, tickers, output_dir: str = './data'):
        logger.info(f"📊 Tracking insider activity for {len(tickers)} tickers...")
        results = {}
        
        for t in tqdm(tickers, desc="Tracking insiders"):
            activities = self.get_insider_activity(t)
            if activities:
                # Score: Big purchases get more points
                score = 0
                for a in activities:
                    if a['value'] > 1000000:
                        score += 30
                    elif a['value'] > 500000:
                        score += 20
                    elif a['value'] > 100000:
                        score += 10
                    else:
                        score += 5
                
                results[t] = {
                    'score': min(score, 100),
                    'total_buys': len(activities),
                    'total_value': sum(a['value'] for a in activities),
                    'transactions': activities[:5]
                }
        
        output = {
            'timestamp': datetime.now().isoformat(),
            'total_with_insider_buys': len(results),
            'details': results
        }
        
        output_file = os.path.join(output_dir, 'insider_moves.json')
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)
        logger.info(f"✅ Saved {len(results)} insider records to {output_file}")


if __name__ == "__main__":
    # Default: Top stocks
    default_tickers = ['AAPL', 'NVDA', 'TSLA', 'MSFT', 'AMZN', 'META', 'GOOGL', 
                       'JPM', 'V', 'MA', 'UNH', 'JNJ', 'XOM', 'PG', 'HD',
                       'BAC', 'ABBV', 'LLY', 'AVGO', 'MRK']
    InsiderTracker().analyze_tickers(default_tickers)
