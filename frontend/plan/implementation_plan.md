# Goal Description
Implement the frontend dashboard for the US stock analysis system using the provided Python Flask backend (`flask_app.py`) and HTML/JS frontend (`templates/index.html`). This completes PARTS 4~6 of the project to create a web interface to view stock analysis, market indices, portfolio status, and AI-driven market insights.

## Proposed Changes

### Web Server (Flask App)
*   **[NEW]** `backend/flask_app.py`
    *   Creates a Flask server setup with API endpoints (e.g., `/api/us/portfolio`, `/api/us/smart-money`, `/api/us/stock-chart/<ticker>`).
    *   Serves standard HTTP methods for fetching real-time data, macro analysis, ETF flow analysis, and technical indicators.
*   **[MODIFY]** [backend/requirements.txt](file:///Users/harvey/Desktop/personal/project/usMarketDashboard/backend/requirements.txt)
    *   Verify & add necessary packages like `Flask`, `ta`, etc. required by the newly created `flask_app.py`.

### Frontend UI & Logic
*   **[NEW]** `backend/templates/index.html`
    *   Combines the HTML document structure, Tailwind CSS styling, and embedded JavaScript logic provided in [PART5_Frontend_UI.md](file:///Users/harvey/Desktop/personal/project/usMarketDashboard/PART5_Frontend_UI.md) and [PART6_Frontend_Logic.md](file:///Users/harvey/Desktop/personal/project/usMarketDashboard/PART6_Frontend_Logic.md).
    *   Contains full features including Charting capabilities using `LightweightCharts` and `ApexCharts`.

## Verification Plan

### Automated Tests
1. Verify syntax and successful runtime of `flask_app.py`:
   `python backend/flask_app.py` (Let it run for a few seconds to verify no instant crashes or import errors)
2. Use `curl` or `read_url_content` tool to test the main page `http://localhost:5001/` to ensure it renders correctly.

### Manual Verification
1. I will ask the user to open the browser at `http://localhost:5001` and manually verify the dashboard UI style, layout, charting capabilities, and data accuracy.
