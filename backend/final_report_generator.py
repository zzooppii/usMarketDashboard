#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final Top 10 Report Generator
Combines Quant Score + AI Bonus for final investment recommendations
"""

import os
import json
import logging
import pandas as pd
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class FinalReportGenerator:
    def __init__(self, data_dir='./data'):
        self.data_dir = data_dir
        
    def run(self, top_n=10):
        logger.info(f"🚀 Generating Final Top {top_n} Report...")
        
        # Load Quant Data
        stats_path = os.path.join(self.data_dir, 'smart_money_picks_v2.csv')
        if not os.path.exists(stats_path):
            logger.error(f"❌ {stats_path} not found.")
            return
        df = pd.read_csv(stats_path)
        
        # Load AI Data
        ai_path = os.path.join(self.data_dir, 'ai_summaries.json')
        ai_data = {}
        if os.path.exists(ai_path):
            with open(ai_path) as f:
                ai_data = json.load(f)
        else:
            logger.warning("⚠️ AI summaries not found. Using quant-only scores.")
            
        results = []
        for _, row in df.iterrows():
            ticker = row['ticker']
            
            # Get AI summary if available
            summary = ''
            if ticker in ai_data:
                summary = ai_data[ticker].get('summary', '')
            
            # AI Bonus Score
            ai_score = 0

            # 1순위: AI 요약 텍스트에서 판단
            if summary:
                if "적극" in summary or "strong buy" in summary.lower():
                    ai_score = 20
                    rec = "Strong Buy"
                elif "매수" in summary or "buy" in summary.lower():
                    ai_score = 10
                    rec = "Buy"
                elif "매도" in summary or "sell" in summary.lower():
                    ai_score = -10
                    rec = "Sell"
                else:
                    rec = "Hold"
            else:
                # 2순위: CSV 애널리스트 추천 컬럼 활용 (AI 요약 없을 때 fallback)
                yf_rec = str(row.get('recommendation', '')).lower()
                rec_map = {
                    'strongbuy': 'Strong Buy',
                    'buy': 'Buy',
                    'hold': 'Hold',
                    'sell': 'Sell',
                    'strongsell': 'Sell',
                }
                rec = rec_map.get(yf_rec, 'Hold')
                if rec == 'Strong Buy': ai_score = 15
                elif rec == 'Buy': ai_score = 8
                    
            final_score = row['composite_score'] * 0.8 + ai_score
            
            results.append({
                'ticker': ticker,
                'name': row.get('name', ticker),
                'final_score': round(final_score, 1),
                'quant_score': row['composite_score'],
                'ai_recommendation': rec,
                'current_price': row.get('current_price', 0),
                'price_at_analysis': row.get('current_price', 0),  # flask_app이 읽는 필드명
                'ai_summary': summary,
                'ai_summary_en': ai_data.get(ticker, {}).get('summary_en', ''),
                'sector': row.get('sector', 'N/A'),
                'grade': row.get('grade', 'N/A'),
                'sd_score': row.get('sd_score', 0),
                'tech_score': row.get('tech_score', 0),
                'fund_score': row.get('fund_score', 0),
                'target_upside': row.get('target_upside', 0),
            })
            
        # Sort and Rank
        results.sort(key=lambda x: x['final_score'], reverse=True)
        top_picks = results[:top_n]
        for i, p in enumerate(top_picks, 1):
            p['rank'] = i
        
        # Save Full Report
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_analyzed': len(results),
            'top_picks': top_picks,
            'all_picks': results
        }
        
        with open(os.path.join(self.data_dir, 'final_top10_report.json'), 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        # Save simplified for Dashboard
        with open(os.path.join(self.data_dir, 'smart_money_current.json'), 'w', encoding='utf-8') as f:
            json.dump({'timestamp': datetime.now().isoformat(), 'picks': top_picks}, f, indent=2, ensure_ascii=False)
            
        logger.info(f"✅ Generated Final Report for {len(top_picks)} stocks")
        
        # Print top picks
        print(f"\n🏆 TOP {top_n} FINAL PICKS:")
        for p in top_picks:
            print(f"   #{p['rank']} {p['ticker']} ({p['name']}): "
                  f"Final {p['final_score']} | Quant {p['quant_score']} | {p['ai_recommendation']}")

if __name__ == "__main__":
    FinalReportGenerator().run()
