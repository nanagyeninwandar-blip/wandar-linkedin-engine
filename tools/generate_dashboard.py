"""
generate_dashboard.py — Reads analytics data and generates a local HTML dashboard.
Usage: python tools/generate_dashboard.py analytics/
Output: dashboard/index.html
"""

import sys
import csv
import re
import json
from pathlib import Path
from datetime import datetime


def parse_csv(path):
    rows = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def parse_manual_input(path):
    text = path.read_text(encoding="utf-8")
    rows = []
    table_started = False
    headers = []
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("|") and line.endswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if not table_started and "Date" in cells[0]:
                headers = [c.lower().replace(" ", "_") for c in cells]
                table_started = True
            elif table_started and re.match(r"^[-| :]+$", line.replace("|", "").strip()):
                continue
            elif table_started and cells[0] not in ["", "---"]:
                row = dict(zip(headers, cells))
                rows.append(row)
    return rows


def build_weekly_metrics(rows):
    weeks = {}
    for row in rows:
        week = row.get("week_of", row.get("date", "Unknown"))
        if week not in weeks:
            weeks[week] = {
                "operator_conversations": 0,
                "saves": 0,
                "reposts": 0,
                "impressions": 0,
                "comments": 0,
                "operator_comments": 0,
                "dms": 0,
            }
        def safe_int(val):
            try:
                return int(str(val).strip() or "0")
            except ValueError:
                return 0

        weeks[week]["saves"] += safe_int(row.get("saves", 0))
        weeks[week]["reposts"] += safe_int(row.get("reposts", 0))
        weeks[week]["impressions"] += safe_int(row.get("impressions", 0))
        weeks[week]["comments"] += safe_int(row.get("comments", 0))
        weeks[week]["operator_comments"] += safe_int(row.get("operator_comments", 0))
        weeks[week]["dms"] += safe_int(row.get("dms_triggered", 0))
        weeks[week]["operator_conversations"] += (
            safe_int(row.get("operator_comments", 0)) + safe_int(row.get("dms_triggered", 0))
        )
    return weeks


def generate_html(weeks_data):
    labels = list(weeks_data.keys())
    op_convos = [weeks_data[w]["operator_conversations"] for w in labels]
    saves = [weeks_data[w]["saves"] for w in labels]
    reposts = [weeks_data[w]["reposts"] for w in labels]
    impressions = [weeks_data[w]["impressions"] for w in labels]
    op_comments = [weeks_data[w]["operator_comments"] for w in labels]

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Wandar — LinkedIn Intelligence Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Segoe UI', system-ui, sans-serif; background: #F5F5F0; color: #1A1A2E; }}
  header {{ background: #1A1A2E; color: #fff; padding: 24px 40px; }}
  header h1 {{ font-size: 22px; font-weight: 700; letter-spacing: -0.5px; }}
  header p {{ font-size: 13px; opacity: 0.6; margin-top: 4px; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px; padding: 32px 40px; }}
  .card {{ background: #fff; border-radius: 8px; padding: 24px; box-shadow: 0 1px 4px rgba(0,0,0,0.07); }}
  .card h2 {{ font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; color: #E8A020; margin-bottom: 16px; }}
  .metric-row {{ display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid #F0F0EC; }}
  .metric-row:last-child {{ border-bottom: none; }}
  .metric-label {{ font-size: 13px; color: #555; }}
  .metric-value {{ font-size: 18px; font-weight: 700; color: #1A1A2E; }}
  .chart-card {{ grid-column: span 2; }}
  canvas {{ max-height: 260px; }}
  .updated {{ text-align: right; padding: 12px 40px; font-size: 11px; color: #999; }}
</style>
</head>
<body>
<header>
  <h1>Wandar — LinkedIn Intelligence Dashboard</h1>
  <p>5 target metrics. Updated every Saturday via the Learning Loop.</p>
</header>

<div class="grid">
  <div class="card">
    <h2>This week</h2>
    <div class="metric-row">
      <span class="metric-label">Operator Conversations</span>
      <span class="metric-value">{op_convos[-1] if op_convos else 0}</span>
    </div>
    <div class="metric-row">
      <span class="metric-label">Conversation Quality (operator comments)</span>
      <span class="metric-value">{op_comments[-1] if op_comments else 0}</span>
    </div>
    <div class="metric-row">
      <span class="metric-label">Saves</span>
      <span class="metric-value">{saves[-1] if saves else 0}</span>
    </div>
    <div class="metric-row">
      <span class="metric-label">Relevant Impressions (total)</span>
      <span class="metric-value">{impressions[-1] if impressions else 0}</span>
    </div>
    <div class="metric-row">
      <span class="metric-label">Reposts</span>
      <span class="metric-value">{reposts[-1] if reposts else 0}</span>
    </div>
  </div>

  <div class="card">
    <h2>Qualified Operator Conversations — Trend</h2>
    <canvas id="convChart"></canvas>
  </div>

  <div class="card">
    <h2>Saves — Trend</h2>
    <canvas id="savesChart"></canvas>
  </div>

  <div class="card">
    <h2>Reposts — Trend</h2>
    <canvas id="repostsChart"></canvas>
  </div>

  <div class="card chart-card">
    <h2>Impressions — Trend</h2>
    <canvas id="impressionsChart"></canvas>
  </div>
</div>

<p class="updated">Last updated: {datetime.now().strftime('%B %d, %Y at %H:%M')}</p>

<script>
const labels = {json.dumps(labels)};
const colors = {{ line: '#E8A020', fill: 'rgba(232, 160, 32, 0.1)', grid: '#F0F0EC' }};

function makeChart(id, label, data) {{
  new Chart(document.getElementById(id), {{
    type: 'line',
    data: {{
      labels,
      datasets: [{{ label, data, borderColor: colors.line, backgroundColor: colors.fill, borderWidth: 2, pointRadius: 4, fill: true, tension: 0.3 }}]
    }},
    options: {{
      responsive: true,
      plugins: {{ legend: {{ display: false }} }},
      scales: {{
        x: {{ grid: {{ color: colors.grid }}, ticks: {{ font: {{ size: 11 }} }} }},
        y: {{ grid: {{ color: colors.grid }}, ticks: {{ font: {{ size: 11 }} }}, beginAtZero: true }}
      }}
    }}
  }});
}}

makeChart('convChart', 'Operator Conversations', {json.dumps(op_convos)});
makeChart('savesChart', 'Saves', {json.dumps(saves)});
makeChart('repostsChart', 'Reposts', {json.dumps(reposts)});
makeChart('impressionsChart', 'Impressions', {json.dumps(impressions)});
</script>
</body>
</html>"""
    return html


def main():
    analytics_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("analytics")
    dashboard_path = Path("dashboard/index.html")
    dashboard_path.parent.mkdir(exist_ok=True)

    all_rows = []

    csv_file = analytics_dir / "linkedin-export.csv"
    if csv_file.exists():
        all_rows.extend(parse_csv(csv_file))
        print(f"Loaded CSV: {csv_file}")

    manual_file = analytics_dir / "manual-input.md"
    if manual_file.exists():
        all_rows.extend(parse_manual_input(manual_file))
        print(f"Loaded manual input: {manual_file}")

    if not all_rows:
        print("No analytics data found. Drop linkedin-export.csv or fill manual-input.md first.")
        dashboard_path.write_text("<html><body><p>No analytics data yet.</p></body></html>")
        return

    weeks_data = build_weekly_metrics(all_rows)
    html = generate_html(weeks_data)
    dashboard_path.write_text(html, encoding="utf-8")
    print(f"Dashboard generated: {dashboard_path}")
    print(f"Open in browser: file:///{dashboard_path.resolve()}")


if __name__ == "__main__":
    main()
