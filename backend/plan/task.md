# 미국주식분석 대시보드 백엔드 구현

## PART 1: 데이터 수집 (4개 스크립트)
- [x] [create_us_daily_prices.py](file:///Users/harvey/Desktop/personal/project/%EB%AF%B8%EA%B5%AD%EC%A3%BC%EC%8B%9D%EB%B6%84%EC%84%9D%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C/backend/create_us_daily_prices.py) — S&P 500 가격 데이터 수집
- [x] [analyze_volume.py](file:///Users/harvey/Desktop/personal/project/%EB%AF%B8%EA%B5%AD%EC%A3%BC%EC%8B%9D%EB%B6%84%EC%84%9D%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C/backend/analyze_volume.py) — 거래량/수급 분석 (OBV, A/D Line, MFI)
- [x] [analyze_13f.py](file:///Users/harvey/Desktop/personal/project/%EB%AF%B8%EA%B5%AD%EC%A3%BC%EC%8B%9D%EB%B6%84%EC%84%9D%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C/backend/analyze_13f.py) — SEC 13F 기관 보유 분석
- [x] [analyze_etf_flows.py](file:///Users/harvey/Desktop/personal/project/%EB%AF%B8%EA%B5%AD%EC%A3%BC%EC%8B%9D%EB%B6%84%EC%84%9D%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C/backend/analyze_etf_flows.py) — ETF 자금 흐름 분석

## PART 2: 분석 및 스크리닝 (5개 스크립트)
- [x] [smart_money_screener_v2.py](file:///Users/harvey/Desktop/personal/project/%EB%AF%B8%EA%B5%AD%EC%A3%BC%EC%8B%9D%EB%B6%84%EC%84%9D%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C/backend/smart_money_screener_v2.py) — 6팩터 종합 스크리닝
- [x] [sector_heatmap.py](file:///Users/harvey/Desktop/personal/project/%EB%AF%B8%EA%B5%AD%EC%A3%BC%EC%8B%9D%EB%B6%84%EC%84%9D%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C/backend/sector_heatmap.py) — 섹터별 퍼포먼스 히트맵
- [x] [options_flow.py](file:///Users/harvey/Desktop/personal/project/%EB%AF%B8%EA%B5%AD%EC%A3%BC%EC%8B%9D%EB%B6%84%EC%84%9D%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C/backend/options_flow.py) — 옵션 플로우 분석
- [x] [insider_tracker.py](file:///Users/harvey/Desktop/personal/project/%EB%AF%B8%EA%B5%AD%EC%A3%BC%EC%8B%9D%EB%B6%84%EC%84%9D%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C/backend/insider_tracker.py) — 인사이더 매매 추적
- [x] [portfolio_risk.py](file:///Users/harvey/Desktop/personal/project/%EB%AF%B8%EA%B5%AD%EC%A3%BC%EC%8B%9D%EB%B6%84%EC%84%9D%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C/backend/portfolio_risk.py) — 포트폴리오 리스크 분석

## PART 3: AI 분석 (5개 스크립트)
- [x] [macro_analyzer.py](file:///Users/harvey/Desktop/personal/project/%EB%AF%B8%EA%B5%AD%EC%A3%BC%EC%8B%9D%EB%B6%84%EC%84%9D%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C/backend/macro_analyzer.py) — 매크로 경제 AI 분석
- [x] [ai_summary_generator.py](file:///Users/harvey/Desktop/personal/project/%EB%AF%B8%EA%B5%AD%EC%A3%BC%EC%8B%9D%EB%B6%84%EC%84%9D%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C/backend/ai_summary_generator.py) — 개별 종목 AI 요약
- [x] [final_report_generator.py](file:///Users/harvey/Desktop/personal/project/%EB%AF%B8%EA%B5%AD%EC%A3%BC%EC%8B%9D%EB%B6%84%EC%84%9D%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C/backend/final_report_generator.py) — 최종 Top 10 리포트
- [x] [economic_calendar.py](file:///Users/harvey/Desktop/personal/project/%EB%AF%B8%EA%B5%AD%EC%A3%BC%EC%8B%9D%EB%B6%84%EC%84%9D%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C/backend/economic_calendar.py) — 경제 캘린더 + AI 전망
- [x] [update_all.py](file:///Users/harvey/Desktop/personal/project/%EB%AF%B8%EA%B5%AD%EC%A3%BC%EC%8B%9D%EB%B6%84%EC%84%9D%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C/backend/update_all.py) — 전체 통합 업데이트

## 환경 설정
- [x] [.env.example](file:///Users/harvey/Desktop/personal/project/%EB%AF%B8%EA%B5%AD%EC%A3%BC%EC%8B%9D%EB%B6%84%EC%84%9D%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C/backend/.env.example) 파일 생성 (API 키 템플릿)
- [x] [requirements.txt](file:///Users/harvey/Desktop/personal/project/%EB%AF%B8%EA%B5%AD%EC%A3%BC%EC%8B%9D%EB%B6%84%EC%84%9D%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C/backend/requirements.txt) 생성
- [x] 프로젝트 디렉토리 구조 세팅

## 검증
- [x] 14개 스크립트 Python 구문 검증 통과 (14 OK, 0 FAIL)
