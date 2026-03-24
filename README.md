# US Market Dashboard

S&P 500 종목 대상의 스마트머니 스크리닝, AI 매크로 분석, 섹터 히트맵을 제공하는 개인용 주식 분석 대시보드입니다.

## 주요 기능

- **Smart Money Picks** — 거래량/기술적/기본적/애널리스트/상대강도 6팩터 복합 스코어링
- **Sector Heatmap** — 11개 S&P 섹터 ETF 실시간 퍼포먼스
- **Options Flow** — 주요 종목 풋콜 비율 및 이상 거래 감지
- **Macro Analysis** — VIX, 금리, 원자재 등 거시지표 수집 + Gemini AI 시장 전망
- **Economic Calendar** — 주요 미국 경제 이벤트 + AI 영향도 분석
- **Insider Tracker** — SEC EDGAR 기반 임원 매매 추적
- **Portfolio Risk** — 상관관계 행렬 및 포트폴리오 변동성 분석
- **Technical Indicators** — RSI, MACD, 볼린저밴드, 지지/저항선 (차트 오버레이)
- **Multi-Language Support** — 한국어/English 실시간 전환 및 AI 리서치 지원

## 대시보드 미리보기

![US Market Dashboard Preview](screenshot.png)

## 기술 스택

| 영역 | 기술 |
|------|------|
| Backend | Python 3.9+, Flask |
| Data | yfinance, SEC EDGAR, Google News RSS |
| AI | Google Gemini API (gemini-3-flash-preview) |
| Frontend | Vanilla JS, Tailwind CSS, LightweightCharts, ApexCharts |

## 프로젝트 구조

```
usMarketDashboard/
├── backend/
│   ├── data/                        # 생성 데이터 (gitignore)
│   │   ├── history/                 # 날짜별 분석 스냅샷
│   │   ├── smart_money_picks_v2.csv
│   │   ├── macro_analysis.json
│   │   └── ...
│   ├── templates/
│   │   └── index.html               # 대시보드 UI
│   │
│   ├── # PART 1: 데이터 수집
│   ├── create_us_daily_prices.py    # S&P 500 일봉 데이터
│   ├── analyze_volume.py            # OBV, 수급 분석
│   ├── analyze_13f.py               # 기관 보유 분석
│   ├── analyze_etf_flows.py         # ETF 자금 흐름
│   │
│   ├── # PART 2: 스크리닝
│   ├── smart_money_screener_v2.py   # 6팩터 복합 스코어링
│   ├── sector_heatmap.py            # 섹터 히트맵 데이터
│   ├── options_flow.py              # 옵션 플로우
│   ├── insider_tracker.py           # 인사이더 매매
│   ├── portfolio_risk.py            # 리스크 분석
│   │
│   ├── # PART 3: AI 분석
│   ├── macro_analyzer.py            # 거시경제 AI 분석
│   ├── ai_summary_generator.py      # 종목별 AI 요약
│   ├── final_report_generator.py    # Top 10 최종 리포트
│   ├── economic_calendar.py         # 경제 캘린더
│   │
│   ├── flask_app.py                 # REST API 서버
│   ├── update_all.py                # 전체 파이프라인 실행
│   └── requirements.txt
└── .gitignore
```

## 데이터 파이프라인

```
[PART 1] 데이터 수집
  create_us_daily_prices.py  →  us_daily_prices.csv
  analyze_volume.py          →  us_volume_analysis.csv
  analyze_13f.py             →  us_13f_holdings.csv
  analyze_etf_flows.py       →  us_etf_flows.csv
         ↓
[PART 2] 스크리닝
  smart_money_screener_v2.py →  smart_money_picks_v2.csv
  sector_heatmap.py          →  sector_heatmap.json
  options_flow.py            →  options_flow.json
  insider_tracker.py         →  insider_moves.json
  portfolio_risk.py          →  portfolio_risk.json
         ↓
[PART 3] AI 분석
  ai_summary_generator.py   →  ai_summaries.json
  final_report_generator.py →  smart_money_current.json
  macro_analyzer.py         →  macro_analysis.json
  economic_calendar.py      →  weekly_calendar.json
         ↓
[Flask API] → [대시보드 UI]
```

## 설치 및 실행

### 1. 환경 설정

```bash
cd backend

# Python 3.9 이상 가상환경 생성
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. API 키 설정

```bash
cp ../.env.example .env
```

`.env` 파일을 열어 키 입력:

```env
GOOGLE_API_KEY=your_gemini_api_key    # 필수 (AI 분석)
OPENAI_API_KEY=your_openai_api_key    # 선택
FRED_API_KEY=your_fred_api_key        # 선택
```

> Gemini API 키 발급: [Google AI Studio](https://aistudio.google.com/app/apikey)

### 3. 데이터 수집 및 분석 실행

```bash
# 전체 파이프라인 실행 (최초 실행 또는 전체 업데이트)
.venv/bin/python update_all.py

# AI 분석 제외하고 빠르게 실행
.venv/bin/python update_all.py --quick

# 데이터 수집만
.venv/bin/python update_all.py --data-only

# AI 분석만 (데이터가 이미 있을 때)
.venv/bin/python update_all.py --ai-only
```

> 전체 파이프라인 소요 시간: 약 30~60분 (네트워크 상태에 따라 다름)

### 4. 서버 실행

```bash
.venv/bin/python flask_app.py
```

브라우저에서 `http://localhost:5001` 접속

## API 엔드포인트

| 엔드포인트 | 설명 |
|-----------|------|
| `GET /api/us/portfolio` | 시장 지수 (S&P500, NASDAQ 등) |
| `GET /api/us/smart-money` | 스마트머니 Top 20 종목 |
| `GET /api/us/stock-chart/<ticker>` | OHLC 차트 데이터 |
| `GET /api/us/technical-indicators/<ticker>` | RSI, MACD, 볼린저밴드 |
| `GET /api/us/sector-heatmap` | 섹터 퍼포먼스 |
| `GET /api/us/macro-analysis` | 거시지표 + AI 분석 |
| `GET /api/us/options-flow` | 옵션 플로우 |
| `GET /api/us/calendar` | 경제 캘린더 |
| `GET /api/us/history-dates` | 과거 분석 날짜 목록 |
| `GET /api/us/history/<date>` | 특정 날짜 분석 + 현재 수익률 |

## 주요 참고사항

- **데이터 갱신 주기**: `update_all.py`를 매일 장 마감 후 실행 권장
- **Python 버전**: 반드시 `.venv/bin/python` 사용 (시스템 Python 3.6 호환 불가)
- **data/ 디렉토리**: `.gitignore`에 포함되어 있으므로 스크립트 실행으로 직접 생성
- **Gemini 모델**: `gemini-3-flash-preview` 사용 (변경 시 각 스크립트의 URL 수정)
