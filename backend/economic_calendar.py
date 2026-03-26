#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Economic Calendar with AI Impact Analysis
Scrapes events and enriches with Gemini AI analysis
"""

import os
import json
import requests
import logging
from datetime import datetime, timedelta
import pandas as pd
from io import StringIO
from dotenv import load_dotenv

load_dotenv()
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class EconomicCalendar:
    def __init__(self, data_dir='./data'):
        self.output = os.path.join(data_dir, 'weekly_calendar.json')
        
    def get_events(self):
        """Scrape Yahoo Finance Calendar (with fallback)"""
        events = []
        try:
            url = "https://finance.yahoo.com/calendar/economic"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code == 200:
                dfs = pd.read_html(StringIO(resp.text))
                if dfs:
                    df = dfs[0]
                    # Filter US events if Country column exists
                    if 'Country' in df.columns:
                        us = df[df['Country'] == 'US']
                    else:
                        us = df
                    for _, row in us.head(20).iterrows():
                        event_name = row.get('Event', row.iloc[0] if len(row) > 0 else 'Unknown')
                        events.append({
                            'date': datetime.now().strftime('%Y-%m-%d'),
                            'event': str(event_name),
                            'impact': 'Medium',
                            'description': f"Actual: {row.get('Actual', '-')} | Est: {row.get('Market Expectation', '-')}"
                        })
        except Exception as e:
            logger.debug(f"Calendar scrape failed: {e}")
        
        # Add Manual Major Events (always include upcoming known events)
        major_events = [
            {'date': '2025-12-10', 'event': 'FOMC Interest Rate Decision',
             'impact': 'High', 'description': 'Fed rate decision and press conference.'},
            {'date': '2025-12-06', 'event': 'US Jobs Report (NFP)',
             'impact': 'High', 'description': 'Non-Farm Payrolls and unemployment rate.'},
            {'date': '2025-12-11', 'event': 'CPI Report',
             'impact': 'High', 'description': 'Consumer Price Index - inflation indicator.'},
        ]
        
        # Only add future events
        today = datetime.now().strftime('%Y-%m-%d')
        for ev in major_events:
            if ev['date'] >= today:
                events.append(ev)
        
        return events
    
    def enrich_ai(self, events):
        """Enrich high-impact events with AI analysis"""
        key = os.getenv('GOOGLE_API_KEY')
        if not key:
            logger.warning("⚠️ No API key for AI enrichment")
            return events
        
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent"
        
        for ev in events:
            if ev['impact'] == 'High':
                try:
                    payload = {
                        "contents": [{"parts": [{"text": f"Explain market impact of: {ev['event']} in 2 sentences."}]}],
                        "generationConfig": {"temperature": 0.5, "maxOutputTokens": 200}
                    }
                    resp = requests.post(f"{url}?key={key}", json=payload, timeout=15)
                    if resp.status_code == 200:
                        ai_text = resp.json()['candidates'][0]['content']['parts'][0]['text']
                        ev['ai_insight'] = ai_text
                        ev['description'] += f"\n\n🤖 AI: {ai_text}"
                except:
                    pass
        return events

    def run(self):
        logger.info("🚀 Generating Economic Calendar...")
        
        events = self.get_events()
        events = self.enrich_ai(events)
        
        output = {
            'updated': datetime.now().isoformat(),
            'events': events,
            'week_start': datetime.now().strftime('%Y-%m-%d'),
            'total_events': len(events),
            'high_impact': len([e for e in events if e['impact'] == 'High'])
        }
        with open(self.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        logger.info(f"✅ Saved {len(events)} events to {self.output}")

if __name__ == "__main__":
    EconomicCalendar().run()
