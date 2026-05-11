"""
read_ssi_sheet.py — Downloads the Wandar SSI Tracker Google Sheet and writes tmp/ssi-data.md.

Usage:
  python tools/read_ssi_sheet.py

Run by the Strategist agent at the start of each pipeline. Writes tmp/ssi-data.md with the
most recent week's SSI scores for the Strategist to read. Exits cleanly if no sheet is
configured or no data rows exist — no crash, just a log message.
"""

import sys
import json
import os
import io
import csv
import tempfile
from pathlib import Path
from datetime import datetime

TOOLS = Path(__file__).parent
ROOT = TOOLS.parent
CONFIG_PATH = TOOLS / "config.json"
OUTPUT_PATH = ROOT / "tmp" / "ssi-data.md"
SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def _get_service():
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    TOKEN_PATH = TOOLS / ".gdrive-token.json"
    CREDENTIALS_PATH = TOOLS / "credentials.json"
    creds = None

    token_json_env = os.environ.get("GDRIVE_TOKEN_JSON")
    if token_json_env:
        creds = Credentials.from_authorized_user_info(json.loads(token_json_env), SCOPES)
    elif TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds_json_env = os.environ.get("GDRIVE_CREDENTIALS_JSON")
            if creds_json_env:
                with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
                    f.write(creds_json_env)
                    tmp = f.name
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(tmp, SCOPES)
                finally:
                    Path(tmp).unlink(missing_ok=True)
            elif CREDENTIALS_PATH.exists():
                flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
            else:
                print("Error: Google Drive credentials not configured.")
                sys.exit(1)
            creds = flow.run_local_server(port=0)
            if not token_json_env:
                TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")

    return build("drive", "v3", credentials=creds)


def get_sheet_id():
    if CONFIG_PATH.exists():
        config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        sheet_id = config.get("gdrive_ssi_sheet_id", "")
        if sheet_id:
            return sheet_id
    print("SSI sheet not configured. Run: python tools/setup_ssi_sheet.py")
    print("Skipping SSI data — tmp/ssi-data.md will not be written.")
    sys.exit(0)


def download_as_csv(sheet_id):
    service = _get_service()
    response = service.files().export(
        fileId=sheet_id,
        mimeType="text/csv",
    ).execute()
    return response.decode("utf-8") if isinstance(response, bytes) else response


def parse_latest_row(csv_text):
    """Return the most recent data row by Date, skipping header and example rows."""
    rows = []
    reader = csv.DictReader(io.StringIO(csv_text))
    for row in reader:
        date_str = row.get("Date", "").strip()
        if not date_str:
            continue
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            continue
        rows.append({k.strip(): v.strip() for k, v in row.items()})

    if not rows:
        return None

    rows.sort(key=lambda r: r.get("Date", ""), reverse=True)
    return rows[0]


def write_ssi_data(row):
    date = row.get("Date", "unknown")
    total = row.get("Total SSI", "?")
    brand = row.get("Professional Brand", "?")
    find = row.get("Find the Right People", "?")
    engage = row.get("Engage with Insights", "?")
    build_rel = row.get("Build Relationships", "?")

    content = f"""# SSI Data — {date}
Total: {total}/100
Professional Brand: {brand}/25
Find the Right People: {find}/25
Engage with Insights: {engage}/25
Build Relationships: {build_rel}/25
"""
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    OUTPUT_PATH.write_text(content, encoding="utf-8")
    print(f"SSI data written to tmp/ssi-data.md (week of {date}, total: {total}/100)")


def main():
    sheet_id = get_sheet_id()
    print(f"Downloading SSI sheet {sheet_id}...")
    csv_text = download_as_csv(sheet_id)
    row = parse_latest_row(csv_text)

    if not row:
        print("No SSI data rows found. Add your weekly scores to the SSI Tracker sheet.")
        print("Skipping SSI data — tmp/ssi-data.md will not be written.")
        sys.exit(0)

    write_ssi_data(row)


if __name__ == "__main__":
    main()
