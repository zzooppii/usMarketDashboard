#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
US ETF Flow Analysis
Tracks fund flows for major ETFs using volume and price momentum as proxies.
Generates AI-powered analysis using Gemini.
"""

import os
import json
import pandas as pd
import numpy as np
import yfinance as yf
import requests
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from tqdm import tqdm
from dotenv import load_dotenv

# Load .env
load_dotenv()
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ETFFlowAnalyzer:
    """Analyze ETF fund flows using volume-based proxies"""
    
    def __init__(self, data_dir: str = '.'):
        self.data_dir = data_dir
        self.output_csv = os.path.join(data_dir, 'us_etf_flows.csv')
        self.output_json = os.path.join(data_dir, 'etf_flow_analysis.json')
        
        # 24 Major ETFs to track
        self.etf_list = {
            # Broad Market
            'SPY': {'name': 'S&P 500', 'category': 'Broad Market'},
            'QQQ': {'name': 'NASDAQ 100', 'category': 'Broad Market'},
            'IWM': {'name': 'Russell 2000', 'category': 'Broad Market'},
            'DIA': {'name': 'Dow Jones', 'category': 'Broad Market'},
            
            # Sector
            'XLK': {'name': 'Technology', 'category': 'Sector'},
            'XLF': {'name': 'Financials', 'category': 'Sector'},
            'XLV': {'name': 'Healthcare', 'category': 'Sector'},
            'XLE': {'name': 'Energy', 'category': 'Sector'},
            'XLY': {'name': 'Consumer Disc.', 'category': 'Sector'},
            'XLP': {'name': 'Consumer Staples', 'category': 'Sector'},
            'XLI': {'name': 'Industrials', 'category': 'Sector'},
            'XLU': {'name': 'Utilities', 'category': 'Sector'},
            
            # Fixed Income
            'TLT': {'name': '20+ Year Treasury', 'category': 'Fixed Income'},
            'IEF': {'name': '7-10 Year Treasury', 'category': 'Fixed Income'},
            'HYG': {'name': 'High Yield Corporate', 'category': 'Fixed Income'},
            'LQD': {'name': 'Investment Grade Corp', 'category': 'Fixed Income'},
            
            # Commodities & Alternatives
            'GLD': {'name': 'Gold', 'category': 'Commodity'},
            'SLV': {'name': 'Silver', 'category': 'Commodity'},
            'USO': {'name': 'Oil', 'category': 'Commodity'},
            
            # International
            'EFA': {'name': 'Developed Markets', 'category': 'International'},
            'EEM': {'name': 'Emerging Markets', 'category': 'International'},
            'FXI': {'name': 'China Large Cap', 'category': 'International'},
            
            # Thematic
            'ARKK': {'name': 'ARK Innovation', 'category': 'Thematic'},
            'SOXX': {'name': 'Semiconductors', 'category': 'Thematic'},
        }
    
    def calculate_flow_proxy(self, df: pd.DataFrame) -> Dict:
        """
        Calculate fund flow proxy using OBV, Volume Ratio, and Price Momentum
        Returns flow score and related metrics
        """
        if len(df) < 20:
            return None
        
        df = df.sort_values('Date').reset_index(drop=True)
        
        close = df['Close']
        volume = df['Volume']
        
        # 1. OBV Trend
        obv = [0]
        for i in range(1, len(df)):
            if close.iloc[i] > close.iloc[i-1]:
                obv.append(obv[-1] + volume.iloc[i])
            elif close.iloc[i] < close.iloc[i-1]:
                obv.append(obv[-1] - volume.iloc[i])
            else:
                obv.append(obv[-1])
        obv = pd.Series(obv, index=df.index)
        
        # OBV change (20-day)
        obv_change = 0
        if len(obv) >= 20 and obv.iloc[-20] != 0:
            obv_change = (obv.iloc[-1] - obv.iloc[-20]) / abs(obv.iloc[-20]) * 100
        
        # 2. Volume Ratio (5d vs 20d)
        vol_5d = volume.tail(5).mean()
        vol_20d = volume.tail(20).mean()
        vol_ratio = vol_5d / vol_20d if vol_20d > 0 else 1
        
        # 3. Price Momentum
        price_5d = (close.iloc[-1] / close.iloc[-5] - 1) * 100 if len(close) >= 5 else 0
        price_20d = (close.iloc[-1] / close.iloc[-20] - 1) * 100 if len(close) >= 20 else 0
        
        # 4. Flow Score (0-100)
        score = 50
        
        # OBV contribution (30%)
        if obv_change > 15:
            score += 15
        elif obv_change > 5:
            score += 10
        elif obv_change > 0:
            score += 5
        elif obv_change < -15:
            score -= 15
        elif obv_change < -5:
            score -= 10
        elif obv_change < 0:
            score -= 5
        
        # Volume ratio contribution (20%)
        if vol_ratio > 1.5:
            score += 10
        elif vol_ratio > 1.2:
            score += 5
        elif vol_ratio < 0.7:
            score -= 10
        elif vol_ratio < 0.8:
            score -= 5
        
        # Price momentum contribution (30%)
        if price_5d > 3:
            score += 10
        elif price_5d > 1:
            score += 5
        elif price_5d < -3:
            score -= 10
        elif price_5d < -1:
            score -= 5
        
        if price_20d > 5:
            score += 5
        elif price_20d < -5:
            score -= 5
        
        score = max(0, min(100, score))
        
        # Determine flow direction
        if score >= 70:
            flow_direction = "Strong Inflow"
        elif score >= 55:
            flow_direction = "Inflow"
        elif score >= 45:
            flow_direction = "Neutral"
        elif score >= 30:
            flow_direction = "Outflow"
        else:
            flow_direction = "Strong Outflow"
        
        return {
            'current_price': round(close.iloc[-1], 2),
            'price_change_5d': round(price_5d, 2),
            'price_change_20d': round(price_20d, 2),
            'volume_ratio': round(vol_ratio, 2),
            'obv_change_20d': round(obv_change, 2),
            'flow_score': round(score, 1),
            'flow_direction': flow_direction,
            'avg_volume_20d': int(vol_20d),
        }
    
    def collect_etf_data(self) -> pd.DataFrame:
        """Collect data for all ETFs"""
        logger.info(f"📊 Collecting data for {len(self.etf_list)} ETFs...")
        
        results = []
        
        for ticker, info in tqdm(self.etf_list.items(), desc="Analyzing ETFs"):
            try:
                etf = yf.Ticker(ticker)
                hist = etf.history(period='3mo')
                
                if hist.empty or len(hist) < 20:
                    logger.debug(f"Skipping {ticker}: insufficient data")
                    continue
                
                hist = hist.reset_index()
                flow_data = self.calculate_flow_proxy(hist)
                
                if flow_data:
                    result = {
                        'ticker': ticker,
                        'name': info['name'],
                        'category': info['category'],
                        **flow_data
                    }
                    results.append(result)
                    
            except Exception as e:
                logger.debug(f"Error processing {ticker}: {e}")
                continue
        
        return pd.DataFrame(results)
    
    def generate_ai_analysis(self, results_df: pd.DataFrame) -> Optional[str]:
        """Generate AI analysis of ETF flows using Gemini"""
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            logger.warning("⚠️ GOOGLE_API_KEY not set. Skipping AI analysis.")
            return None
        
        # Build prompt
        inflows = results_df[results_df['flow_score'] >= 55].sort_values('flow_score', ascending=False)
        outflows = results_df[results_df['flow_score'] < 45].sort_values('flow_score')
        
        inflow_txt = "\n".join([
            f"- {row['name']} ({row['ticker']}): Score {row['flow_score']}, "
            f"Price 5d: {row['price_change_5d']}%, Vol Ratio: {row['volume_ratio']}"
            for _, row in inflows.head(10).iterrows()
        ])
        
        outflow_txt = "\n".join([
            f"- {row['name']} ({row['ticker']}): Score {row['flow_score']}, "
            f"Price 5d: {row['price_change_5d']}%, Vol Ratio: {row['volume_ratio']}"
            for _, row in outflows.head(10).iterrows()
        ])
        
        prompt = f"""ETF 자금 흐름 분석 결과를 해석해주세요.

자금 유입 ETF:
{inflow_txt}

자금 유출 ETF:
{outflow_txt}

요청:
1. 현재 자금 흐름의 핵심 트렌드 (2-3줄)
2. Risk-On vs Risk-Off 판단
3. 섹터 로테이션 분석
4. 투자 시사점 (3줄 이내)

한국어로 간결하게 작성해주세요."""

        try:
            url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4096}
            }
            resp = requests.post(f"{url}?key={api_key}", json=payload, timeout=30)
            if resp.status_code == 200:
                return resp.json()['candidates'][0]['content']['parts'][0]['text']
            else:
                logger.warning(f"Gemini API error: {resp.status_code}")
                return None
        except Exception as e:
            logger.error(f"AI analysis error: {e}")
            return None
    
    def run(self) -> pd.DataFrame:
        """Run full ETF flow analysis"""
        logger.info("🚀 Starting ETF Flow Analysis...")
        
        # 1. Collect data
        results_df = self.collect_etf_data()
        
        if results_df.empty:
            logger.error("❌ No ETF data collected")
            return pd.DataFrame()
        
        # 2. Save CSV
        results_df.to_csv(self.output_csv, index=False)
        logger.info(f"✅ Saved {len(results_df)} ETFs to {self.output_csv}")
        
        # 3. Generate AI analysis
        ai_analysis = self.generate_ai_analysis(results_df)
        
        # 4. Save JSON with AI analysis
        output = {
            'timestamp': datetime.now().isoformat(),
            'total_etfs': len(results_df),
            'summary': {
                'strong_inflow': len(results_df[results_df['flow_direction'] == 'Strong Inflow']),
                'inflow': len(results_df[results_df['flow_direction'] == 'Inflow']),
                'neutral': len(results_df[results_df['flow_direction'] == 'Neutral']),
                'outflow': len(results_df[results_df['flow_direction'] == 'Outflow']),
                'strong_outflow': len(results_df[results_df['flow_direction'] == 'Strong Outflow']),
            },
            'ai_analysis': ai_analysis or "AI 분석을 사용하려면 GOOGLE_API_KEY를 설정하세요.",
            'etf_flows': results_df.to_dict(orient='records')
        }
        
        with open(self.output_json, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        logger.info(f"✅ Saved analysis to {self.output_json}")
        
        # 5. Print summary
        logger.info("\n📊 ETF Flow Summary:")
        for direction in ['Strong Inflow', 'Inflow', 'Neutral', 'Outflow', 'Strong Outflow']:
            count = len(results_df[results_df['flow_direction'] == direction])
            logger.info(f"   {direction}: {count} ETFs")
        
        return results_df


def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description='ETF Flow Analysis')
    parser.add_argument('--dir', default='./data', help='Data directory')
    args = parser.parse_args()
    
    analyzer = ETFFlowAnalyzer(data_dir=args.dir)
    results = analyzer.run()
    
    if not results.empty:
        print("\n📈 Top Inflow ETFs:")
        top = results.nlargest(5, 'flow_score')
        for _, row in top.iterrows():
            print(f"   {row['ticker']} ({row['name']}): Score {row['flow_score']} | "
                  f"5d: {row['price_change_5d']}%")
        
        print("\n📉 Top Outflow ETFs:")
        bottom = results.nsmallest(5, 'flow_score')
        for _, row in bottom.iterrows():
            print(f"   {row['ticker']} ({row['name']}): Score {row['flow_score']} | "
                  f"5d: {row['price_change_5d']}%")


if __name__ == "__main__":
    main()
