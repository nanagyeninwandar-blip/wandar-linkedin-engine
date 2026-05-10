"""
read_analytics_sheet.py — Downloads the Wandar analytics Google Sheet as CSV and parses it.

Usage:
  python tools/read_analytics_sheet.py           # prints parsed data
  python tools/read_analytics_sheet.py --csv     # prints raw CSV
  import from run_pipeline.py via: from read_analytics_sheet import get_analytics_data

Returns a list of dicts, one per row, matching the sheet columns.
"""

import sys
import json
import os
import io
import csv
from pathlib import Path

TOOLS = Path(__file__).parent
CONFIG_PATH = TOOLS / "config.json"
SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def _get_service():
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    import tempfile

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
        sheet_id = config.get("gdrive_analytics_sheet_id", "")
        if sheet_id:
            return sheet_id
    print("Error: gdrive_analytics_sheet_id not set in tools/config.json")
    print("Run: python tools/setup_analytics_sheet.py")
    sys.exit(1)


def download_as_csv(sheet_id):
    """Download Google Sheet as CSV via Drive export API."""
    service = _get_service()
    response = service.files().export(
        fileId=sheet_id,
        mimeType="text/csv",
    ).execute()
    return response.decode("utf-8") if isinstance(response, bytes) else response


def parse_csv(csv_text):
    """Parse CSV into list of dicts. Skips the instructions row and empty rows."""
    rows = []
    reader = csv.DictReader(io.StringIO(csv_text))
    for row in reader:
        # Skip instruction rows and empty rows
        week = row.get("Week", "").strip()
        date = row.get("Date", "").strip()
        hook = row.get("Post Hook (first line)", "").strip()
        if not date and not hook:
            continue
        if "WANDAR LinkedIn" in hook or "Fill in" in hook:
            continue
        rows.append({k.strip(): v.strip() for k, v in row.items()})
    return rows


def get_analytics_data():
    """Main entry point for the Learning Loop. Returns list of row dicts."""
    sheet_id = get_sheet_id()
    csv_text = download_as_csv(sheet_id)
    rows = parse_csv(csv_text)
    return rows


def format_for_agent(rows):
    """Format analytics rows as a markdown table for the Learning Loop agent."""
    if not rows:
        return "No analytics data found in the sheet."

    headers = list(rows[0].keys())
    lines = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for row in rows:
        lines.append("| " + " | ".join(row.get(h, "") for h in headers) + " |")
    return "\n".join(lines)


if __name__ == "__main__":
    raw_mode = "--csv" in sys.argv
    sheet_id = get_sheet_id()
    print(f"Downloading sheet {sheet_id}...")
    csv_text = download_as_csv(sheet_id)

    if raw_mode:
        print(csv_text)
    else:
        rows = parse_csv(csv_text)
        if not rows:
            print("No data rows found in the sheet yet.")
        else:
            print(f"Found {len(rows)} data rows.\n")
            print(format_for_agent(rows))
