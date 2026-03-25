#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Stock Summary Generator
Generates investment summaries using Gemini AI
"""

import os
import json
import logging
import time
import requests
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class NewsCollector:
    def get_news(self, ticker: str):
        # Uses Google News RSS
        news = []
        try:
            import xml.etree.ElementTree as ET
            url = f"https://news.google.com/rss/search?q={ticker}+stock&hl=en-US&gl=US&ceid=US:en"
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                root = ET.fromstring(resp.content)
                for item in root.findall('.//item')[:3]:
                    news.append({
                        'title': item.find('title').text,
                        'published': item.find('pubDate').text if item.find('pubDate') is not None else ''
                    })
        except:
            pass
        return news


class GeminiGenerator:
    def __init__(self):
        self.key = os.getenv('GOOGLE_API_KEY')
        self.url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent"
        
    def generate(self, ticker, data, news, lang='ko'):
        if not self.key:
            return "No API Key"
        
        news_txt = "\n".join([n['title'] for n in news])
        score_info = f"Score: {data.get('composite_score')}/100, Quant: {data.get('grade')}"
        
        if lang == 'ko':
            prompt = f"""종목: {ticker}
정보: {score_info}
뉴스: {news_txt}
요청: 3-4문장으로 투자 의견 요약 (수급, 펀더멘털, 전략). 이모지 X."""
        else:
            prompt = f"""Stock: {ticker}
Info: {score_info}
News: {news_txt}
Req: 3-4 sentence investment summary. No emojis."""

        try:
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.7, "maxOutputTokens": 1500}
            }
            resp = requests.post(f"{self.url}?key={self.key}", json=payload, timeout=30)
            if resp.status_code == 200:
                return resp.json()['candidates'][0]['content']['parts'][0]['text']
        except:
            pass
        return "Analysis Failed"


class AIStockAnalyzer:
    def __init__(self, data_dir='./data'):
        self.data_dir = data_dir
        self.output = os.path.join(data_dir, 'ai_summaries.json')
        self.gen = GeminiGenerator()
        self.news = NewsCollector()
        
    def run(self, top_n=20):
        logger.info(f"🚀 Generating AI summaries for top {top_n} stocks...")
        
        csv = os.path.join(self.data_dir, 'smart_money_picks_v2.csv')
        if not os.path.exists(csv):
            logger.error(f"❌ {csv} not found. Run smart_money_screener_v2.py first.")
            return
        
        df = pd.read_csv(csv).head(top_n)
        results = {}
        
        # Load existing
        if os.path.exists(self.output):
            with open(self.output) as f:
                results = json.load(f)
            
        for _, row in tqdm(df.iterrows(), total=len(df), desc="Generating AI summaries"):
            ticker = row['ticker']
            if ticker in results:
                continue  # Skip if exists
            
            news = self.news.get_news(ticker)
            summary_ko = self.gen.generate(ticker, row.to_dict(), news, 'ko')
            summary_en = self.gen.generate(ticker, row.to_dict(), news, 'en')
            
            results[ticker] = {
                'summary': summary_ko,
                'summary_ko': summary_ko,
                'summary_en': summary_en,
                'updated': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
            }
            time.sleep(1)  # Rate limit
            
        with open(self.output, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        logger.info(f"✅ Saved {len(results)} summaries to {self.output}")

if __name__ == "__main__":
    AIStockAnalyzer().run()
