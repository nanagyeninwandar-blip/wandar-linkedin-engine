"""
setup_analytics_sheet.py — One-time setup: creates the Wandar analytics Google Sheet on Drive.

Run once:
  python tools/setup_analytics_sheet.py

What it does:
  1. Generates the formatted Excel template (analytics/analytics-tracker.xlsx)
  2. Uploads it to Google Drive with conversion to Google Sheets format
  3. Saves the Sheet ID to tools/config.json as 'gdrive_analytics_sheet_id'
  4. Prints the URL — bookmark it and open it every week to fill in post data

Requirements:
  - Google Drive credentials configured (same as upload_gdrive.py)
  - GDRIVE_TOKEN_JSON env var set (or tools/.gdrive-token.json exists locally)
"""

import sys
import json
import os
from pathlib import Path

TOOLS = Path(__file__).parent
ROOT = TOOLS.parent
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


def main():
    # Step 1: Generate the Excel template
    print("Generating analytics Excel template...")
    sys.path.insert(0, str(TOOLS))
    from generate_analytics_template import make_template
    template_path = make_template()

    # Step 2: Upload to Drive with conversion to Google Sheets
    print("Uploading to Google Drive as Google Sheet...")
    try:
        from googleapiclient.http import MediaFileUpload
    except ImportError:
        print("Error: google-api-python-client not installed. Run: pip install google-api-python-client")
        sys.exit(1)

    service = _get_service()

    # Check if sheet already exists
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8")) if CONFIG_PATH.exists() else {}
    existing_id = config.get("gdrive_analytics_sheet_id", "")

    mime_xlsx = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    mime_sheet = "application/vnd.google-apps.spreadsheet"

    media = MediaFileUpload(str(template_path), mimetype=mime_xlsx, resumable=False)

    if existing_id:
        # Update the existing sheet
        service.files().update(
            fileId=existing_id,
            media_body=media,
        ).execute()
        sheet_id = existing_id
        print(f"Updated existing sheet: {sheet_id}")
    else:
        # Create new sheet with conversion
        metadata = {
            "name": "Wandar LinkedIn Analytics",
            "mimeType": mime_sheet,
        }
        result = service.files().create(
            body=metadata,
            media_body=media,
            fields="id",
        ).execute()
        sheet_id = result["id"]
        print(f"Created new sheet: {sheet_id}")

    # Step 3: Save sheet ID to config.json
    config["gdrive_analytics_sheet_id"] = sheet_id
    CONFIG_PATH.write_text(json.dumps(config, indent=2), encoding="utf-8")
    print(f"Sheet ID saved to tools/config.json")

    # Step 4: Print the URL
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"
    print(f"\n{'='*60}")
    print(f"Analytics sheet ready:")
    print(f"  {url}")
    print(f"{'='*60}")
    print(f"\nBookmark this URL. Open it each week to fill in post performance data.")
    print(f"Then run: python tools/run_pipeline.py (or 'run learning loop' in Claude)")


if __name__ == "__main__":
    main()
