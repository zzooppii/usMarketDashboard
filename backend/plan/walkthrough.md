# 미국주식분석 대시보드 — 백엔드 구현 완료

## 생성된 파일 (16개)

### 디렉토리 구조
```
backend/
├── .env.example              # API 키 템플릿
├── requirements.txt          # Python 패키지 의존성
├── create_us_daily_prices.py # S&P 500 가격 수집
├── analyze_volume.py         # 거래량/수급 분석
├── analyze_13f.py            # 기관 보유 분석
├── analyze_etf_flows.py      # ETF 자금 흐름
├── smart_money_screener_v2.py# 6팩터 종합 스크리닝
├── sector_heatmap.py         # 섹터 히트맵
├── options_flow.py           # 옵션 플로우
├── insider_tracker.py        # 인사이더 매매
├── portfolio_risk.py         # 포트폴리오 리스크
├── macro_analyzer.py         # 매크로 AI 분석
├── ai_summary_generator.py   # 종목 AI 요약
├── final_report_generator.py # 최종 Top 10 리포트
├── economic_calendar.py      # 경제 캘린더
└── update_all.py             # 전체 파이프라인
```

## 검증 결과

| 검증 항목 | 결과 |
|----------|------|
| Python 구문 검증 (14개) | ✅ 14 OK, 0 FAIL |
| 파일 생성 확인 | ✅ 16개 파일 정상 |

## 실행 방법

```bash
# 1. 가상 환경 생성 및 활성화 (Python 3.8+)
cd backend
python -m venv .venv
source .venv/bin/activate

# 2. 패키지 설치
pip install --upgrade pip
pip install -r requirements.txt

# 3. 환경 설정
cp .env.example .env
# .env 파일에 API 키 입력

# 4. 데이터 수집/분석 파이프라인 실행
python update_all.py          # 전체 통합 파이프라인
python update_all.py --quick  # AI 분석 제외 (기본 분석만)
python update_all.py --data-only  # 데이터 수집만 실행

# 5. 프론트엔드 웹 대시보드 서버 실행
python flask_app.py
# 브라우저에서 http://localhost:5001 접속
```

## 출력 파일

| 스크립트 | 출력 |
|---------|------|
| create_us_daily_prices | `us_daily_prices.csv`, `us_stocks_list.csv` |
| analyze_volume | `us_volume_analysis.csv` |
| analyze_13f | `us_13f_holdings.csv` |
| analyze_etf_flows | `us_etf_flows.csv`, `etf_flow_analysis.json` |
| smart_money_screener_v2 | `smart_money_picks_v2.csv` |
| sector_heatmap | `sector_heatmap.json` |
| options_flow | `options_flow.json` |
| insider_tracker | `insider_moves.json` |
| portfolio_risk | `portfolio_risk.json` |
| macro_analyzer | `macro_analysis.json`, `macro_analysis_en.json` |
| ai_summary_generator | `ai_summaries.json` |
| final_report_generator | `final_top10_report.json`, `smart_money_current.json` |
| economic_calendar | `weekly_calendar.json` |
