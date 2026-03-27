#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Options Flow Analyzer
Tracks options volume, Put/Call ratio, and unusual activity
"""

import os
import json
import logging
import yfinance as yf
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class OptionsFlowAnalyzer:
    def __init__(self):
        self.watchlist = ['AAPL', 'NVDA', 'TSLA', 'MSFT', 'AMZN', 'META', 'GOOGL', 'SPY', 'QQQ', 'AMD']
    
    def get_options_summary(self, ticker: str):
        try:
            stock = yf.Ticker(ticker)
            exps = stock.options
            if not exps:
                return {'error': 'No options'}
            
            opt = stock.option_chain(exps[0])
            calls, puts = opt.calls, opt.puts
            
            call_vol = calls['volume'].sum()
            put_vol = puts['volume'].sum()
            call_oi = calls['openInterest'].sum()
            put_oi = puts['openInterest'].sum()
            
            pc_ratio = put_vol / call_vol if call_vol > 0 else 0
            
            # Unusual activity
            avg_call = calls['volume'].mean()
            unusual_calls = len(calls[calls['volume'] > avg_call * 3])
            unusual_puts = len(puts[puts['volume'] > puts['volume'].mean() * 3])
            
            # Sentiment determination
            if pc_ratio < 0.5:
                sentiment = "Very Bullish"
            elif pc_ratio < 0.7:
                sentiment = "Bullish"
            elif pc_ratio < 1.0:
                sentiment = "Neutral"
            elif pc_ratio < 1.3:
                sentiment = "Bearish"
            else:
                sentiment = "Very Bearish"
            
            return {
                'ticker': ticker,
                'expiration': exps[0],
                'metrics': {
                    'pc_ratio': round(pc_ratio, 2),
                    'call_vol': int(call_vol),
                    'put_vol': int(put_vol),
                    'call_oi': int(call_oi),
                    'put_oi': int(put_oi),
                    'sentiment': sentiment
                },
                'unusual': {
                    'calls': unusual_calls,
                    'puts': unusual_puts,
                    'total': unusual_calls + unusual_puts
                }
            }
        except Exception as e:
            return {'ticker': ticker, 'error': str(e)}

    def analyze_watchlist(self, output_dir: str = './data'):
        logger.info(f"📊 Analyzing options for {len(self.watchlist)} tickers...")
        results = []
        for t in self.watchlist:
            res = self.get_options_summary(t)
            if 'error' not in res:
                results.append(res)
                logger.info(f"   {t}: P/C={res['metrics']['pc_ratio']} | {res['metrics']['sentiment']}")
            else:
                logger.debug(f"   {t}: {res.get('error', 'Unknown error')}")
        
        output = {
            'timestamp': datetime.now().isoformat(),
            'total_analyzed': len(results),
            'options_flow': results
        }
        
        output_file = os.path.join(output_dir, 'options_flow.json')
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)
        logger.info(f"✅ Saved to {output_file}")


if __name__ == "__main__":
    OptionsFlowAnalyzer().analyze_watchlist()
