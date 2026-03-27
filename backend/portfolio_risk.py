#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Portfolio Risk Analyzer
Calculates correlation matrix, portfolio volatility, and high-correlation pairs
"""

import os
import json
import logging
import pandas as pd
import numpy as np
import yfinance as yf

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class PortfolioRiskAnalyzer:
    def analyze_portfolio(self, tickers, output_dir: str = './data'):
        logger.info(f"📊 Analyzing portfolio risk for {len(tickers)} tickers...")
        try:
            data = yf.download(tickers, period='6mo', progress=False)['Close']
            returns = data.pct_change().dropna()
            
            # Correlation matrix
            corr = returns.corr()
            high_corr = []
            cols = corr.columns
            for i in range(len(cols)):
                for j in range(i+1, len(cols)):
                    if corr.iloc[i, j] > 0.8:
                        high_corr.append({
                            'pair': [cols[i], cols[j]],
                            'correlation': round(corr.iloc[i, j], 2)
                        })
            
            # Portfolio volatility (equal-weight)
            cov = returns.cov() * 252  # Annualized
            weights = np.array([1/len(tickers)] * len(tickers))
            var = np.dot(weights.T, np.dot(cov, weights))
            vol = np.sqrt(var)
            
            # Individual stock stats
            stock_stats = {}
            for ticker in tickers:
                if ticker in returns.columns:
                    ret = returns[ticker]
                    stock_stats[ticker] = {
                        'annual_return': round(ret.mean() * 252 * 100, 2),
                        'annual_volatility': round(ret.std() * np.sqrt(252) * 100, 2),
                        'sharpe_ratio': round((ret.mean() * 252) / (ret.std() * np.sqrt(252)), 2) if ret.std() > 0 else 0,
                        'max_drawdown': round(((data[ticker] / data[ticker].cummax()) - 1).min() * 100, 2)
                    }
            
            # VaR (95% confidence)
            portfolio_returns = returns.mean(axis=1)
            var_95 = np.percentile(portfolio_returns, 5) * 100
            
            result = {
                'timestamp': pd.Timestamp.now().isoformat(),
                'portfolio': {
                    'tickers': tickers,
                    'num_stocks': len(tickers),
                    'annual_volatility_pct': round(vol * 100, 2),
                    'var_95_daily_pct': round(var_95, 2),
                    'avg_correlation': round(corr.values[np.triu_indices_from(corr.values, k=1)].mean(), 2)
                },
                'high_correlations': high_corr,
                'stock_stats': stock_stats,
                'correlation_matrix': corr.round(2).to_dict()
            }
            
            output_file = os.path.join(output_dir, 'portfolio_risk.json')
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
            logger.info(f"✅ Risk Analysis saved to {output_file}")
            logger.info(f"   Portfolio Volatility: {vol*100:.1f}%")
            logger.info(f"   High Correlation Pairs: {len(high_corr)}")
            logger.info(f"   VaR (95%): {var_95:.2f}%")
            
            return result
            
        except Exception as e:
            logger.error(f"Error: {e}")
            return None


if __name__ == "__main__":
    # Example with top stocks
    PortfolioRiskAnalyzer().analyze_portfolio(
        ['AAPL', 'NVDA', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'JPM']
    )
