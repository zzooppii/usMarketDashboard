#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
US Market Update All - Full Pipeline Runner
Runs all data collection, analysis, and AI scripts sequentially
"""

import os
import sys
import subprocess
import time
import argparse
import logging
import json
import shutil
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Script execution order with descriptions and timeouts
scripts = [
    # PART 1: Data Collection
    ("create_us_daily_prices.py", "📊 Data Collection (S&P 500 Prices)", 600),
    ("analyze_volume.py", "📈 Volume/Supply-Demand Analysis", 300),
    ("analyze_13f.py", "🏦 13F Institutional Analysis", 600),
    ("analyze_etf_flows.py", "💰 ETF Flow Analysis", 300),
    
    # PART 2: Screening & Analysis
    ("smart_money_screener_v2.py", "🔍 Smart Money Screening v2", 600),
    ("sector_heatmap.py", "🗺️ Sector Heatmap", 300),
    ("options_flow.py", "📋 Options Flow Analysis", 300),
    ("insider_tracker.py", "👤 Insider Tracking", 300),
    ("portfolio_risk.py", "⚠️ Portfolio Risk Analysis", 300),
    
    # PART 3: AI Analysis
    ("ai_summary_generator.py", "🤖 AI Summary Generation", 900),
    ("final_report_generator.py", "📝 Final Report Generation", 60),
    ("macro_analyzer.py", "🌍 Macro Analysis", 300),
    ("economic_calendar.py", "📅 Economic Calendar", 300),
]


def run_script(name: str, desc: str, timeout: int) -> bool:
    """Run a single script with timeout"""
    script_path = os.path.join(os.path.dirname(__file__), name)
    
    if not os.path.exists(script_path):
        logger.warning(f"   ⚠️ Script not found: {name}")
        return False
    
    logger.info(f"\n{'='*60}")
    logger.info(f"   {desc}")
    logger.info(f"   Script: {name} (timeout: {timeout}s)")
    logger.info(f"{'='*60}")
    
    start = time.time()
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            timeout=timeout,
            check=True,
            capture_output=True,
            text=True,
            cwd=os.path.dirname(__file__)
        )
        elapsed = time.time() - start
        logger.info(f"   ✅ Done in {elapsed:.1f}s")
        return True
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start
        logger.error(f"   ⏰ Timeout after {elapsed:.1f}s")
        return False
    except subprocess.CalledProcessError as e:
        elapsed = time.time() - start
        logger.error(f"   ❌ Failed after {elapsed:.1f}s: {e}")
        if e.stderr:
            logger.error(f"   stderr: {e.stderr[:500]}")
        return False
    except Exception as e:
        logger.error(f"   ❌ Error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='US Market Full Update Pipeline')
    parser.add_argument('--quick', action='store_true', help='Skip AI analysis scripts')
    parser.add_argument('--data-only', action='store_true', help='Run only data collection (PART 1)')
    parser.add_argument('--ai-only', action='store_true', help='Run only AI analysis (PART 3)')
    args = parser.parse_args()
    
    logger.info("🚀 US Market Full Update Pipeline Starting...")
    logger.info(f"   Mode: {'Quick' if args.quick else 'Data Only' if args.data_only else 'AI Only' if args.ai_only else 'Full'}")
    logger.info(f"   Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Ensure data directory exists before running any scripts
    data_dir = os.path.join(os.path.dirname(__file__), 'data', 'history')
    os.makedirs(data_dir, exist_ok=True)
    logger.info(f"   Data dir: {os.path.dirname(data_dir)}")
    
    start_total = time.time()
    results = {'success': [], 'failed': [], 'skipped': []}
    
    for name, desc, timeout in scripts:
        # Filter based on mode
        if args.quick and "AI" in desc:
            results['skipped'].append(name)
            continue
        if args.data_only and name not in ['create_us_daily_prices.py', 'analyze_volume.py', 'analyze_13f.py', 'analyze_etf_flows.py']:
            results['skipped'].append(name)
            continue
        if args.ai_only and name not in ['ai_summary_generator.py', 'final_report_generator.py', 'macro_analyzer.py', 'economic_calendar.py']:
            results['skipped'].append(name)
            continue
        
        success = run_script(name, desc, timeout)
        if success:
            results['success'].append(name)
        else:
            results['failed'].append(name)
    
    # Summary
    elapsed_total = time.time() - start_total
    logger.info(f"\n{'='*60}")
    logger.info(f"📊 PIPELINE SUMMARY")
    logger.info(f"{'='*60}")
    logger.info(f"   Total time: {elapsed_total/60:.1f} min")
    logger.info(f"   ✅ Success: {len(results['success'])}")
    logger.info(f"   ❌ Failed: {len(results['failed'])}")
    logger.info(f"   ⏭️ Skipped: {len(results['skipped'])}")
    
    if results['failed']:
        logger.warning(f"   Failed scripts: {results['failed']}")

    # Save daily snapshot to history
    current_json = os.path.join(os.path.dirname(__file__), 'data', 'smart_money_current.json')
    if os.path.exists(current_json):
        today = datetime.now().strftime('%Y-%m-%d')
        snapshot_path = os.path.join(os.path.dirname(__file__), 'data', 'history', f'picks_{today}.json')
        shutil.copy2(current_json, snapshot_path)
        logger.info(f"   📸 Snapshot saved: picks_{today}.json")

    logger.info(f"{'='*60}")


if __name__ == "__main__":
    main()
