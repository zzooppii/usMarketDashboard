import os

filepath = '/Users/harvey/Desktop/personal/project/usMarketDashboard/backend/flask_app.py'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("os.path.join('us_market', '", "os.path.join('")
text = text.replace("from us_market.sector_heatmap import", "from sector_heatmap import")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)
print("Paths fixed successfully.")
