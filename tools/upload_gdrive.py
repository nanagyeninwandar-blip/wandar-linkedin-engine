"""
upload_gdrive.py — Uploads pipeline output files to a Google Drive folder.

Usage:
  python tools/upload_gdrive.py <file1> [file2 ...]
  python tools/upload_gdrive.py --all              (uploads all files from latest pipeline run)
  python tools/upload_gdrive.py --all --folder-id <id>  (upload to a specific folder)

One-time setup:
  1. Go to console.cloud.google.com
  2. Create a project → Enable Google Drive API
  3. Credentials → Create → OAuth 2.0 Client ID → Desktop app → Download JSON
  4. Save the downloaded file as tools/credentials.json
  5. Create a folder in Google Drive, copy its ID from the URL
     (the long string after /folders/ in the URL)
  6. Add to tools/config.json: "google_drive_folder_id": "YOUR_FOLDER_ID"
  7. Run this script once — browser opens for consent, token saved automatically.
     All future runs are silent.

GitHub Actions usage:
  Set environment variables:
    GDRIVE_TOKEN_JSON       — contents of tools/.gdrive-token.json
    GDRIVE_CREDENTIALS_JSON — contents of tools/credentials.json
"""

import sys
import json
import os
import mimetypes
from pathlib import Path
from datetime import date

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
TOOLS_DIR = Path(__file__).parent
CONFIG_PATH = TOOLS_DIR / "config.json"
CREDENTIALS_PATH = TOOLS_DIR / "credentials.json"
TOKEN_PATH = TOOLS_DIR / ".gdrive-token.json"

MIME_TYPES = {
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".md":   "text/markdown",
    ".pdf":  "application/pdf",
}


def _check_deps():
    missing = []
    for pkg in ("googleapiclient", "google_auth_oauthlib", "google.auth.transport.requests"):
        try:
            __import__(pkg.split(".")[0])
        except ImportError:
            missing.append(pkg)
    if missing:
        print("Error: missing dependencies. Run:")
        print("  pip install google-api-python-client google-auth-oauthlib google-auth-httplib2")
        sys.exit(1)


def _load_config():
    if not CONFIG_PATH.exists():
        print(f"Error: {CONFIG_PATH} not found.")
        sys.exit(1)
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def _get_service():
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    import tempfile

    creds = None

    # GitHub Actions: load token from environment variable
    token_json_env = os.environ.get("GDRIVE_TOKEN_JSON")
    if token_json_env:
        creds = Credentials.from_authorized_user_info(json.loads(token_json_env), SCOPES)
    elif TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            if not token_json_env:
                TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")
        else:
            creds_json_env = os.environ.get("GDRIVE_CREDENTIALS_JSON")
            if creds_json_env:
                with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
                    f.write(creds_json_env)
                    tmp_path = f.name
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(tmp_path, SCOPES)
                finally:
                    Path(tmp_path).unlink(missing_ok=True)
            elif CREDENTIALS_PATH.exists():
                flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
            else:
                print("Google Drive credentials not configured.")
                print()
                print("One-time setup:")
                print("  1. Go to console.cloud.google.com")
                print("  2. Create project → Enable Google Drive API")
                print("  3. Credentials → OAuth 2.0 Client ID → Desktop app → Download JSON")
                print(f"  4. Save as: {CREDENTIALS_PATH}")
                print("  5. Add to config.json: \"google_drive_folder_id\": \"YOUR_FOLDER_ID\"")
                print("  6. Re-run this script — browser opens once for consent.")
                sys.exit(0)
            creds = flow.run_local_server(port=0)
            if not token_json_env:
                TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")

    return build("drive", "v3", credentials=creds)


def _find_existing(service, folder_id, filename):
    query = (
        f"name = '{filename}' "
        f"and '{folder_id}' in parents "
        f"and trashed = false"
    )
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get("files", [])
    return files[0]["id"] if files else None


def create_or_find_folder(service, folder_name, parent_id):
    query = (
        f"name = '{folder_name}' "
        f"and '{parent_id}' in parents "
        f"and mimeType = 'application/vnd.google-apps.folder' "
        f"and trashed = false"
    )
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get("files", [])
    if files:
        return files[0]["id"]
    metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_id],
    }
    result = service.files().create(body=metadata, fields="id").execute()
    print(f"  Created folder: {folder_name}")
    return result["id"]


def upload_file(service, file_path, folder_id):
    from googleapiclient.http import MediaFileUpload

    file_path = Path(file_path)
    if not file_path.exists():
        print(f"  Skipping (not found): {file_path}")
        return None

    mime = MIME_TYPES.get(file_path.suffix.lower()) or mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
    media = MediaFileUpload(str(file_path), mimetype=mime, resumable=True)
    filename = file_path.name

    existing_id = _find_existing(service, folder_id, filename)

    if existing_id:
        service.files().update(fileId=existing_id, media_body=media).execute()
        url = f"https://drive.google.com/file/d/{existing_id}/view"
        print(f"  Updated: {filename}")
        print(f"    {url}")
        return url
    else:
        metadata = {"name": filename, "parents": [folder_id]}
        result = service.files().create(body=metadata, media_body=media, fields="id").execute()
        file_id = result["id"]
        url = f"https://drive.google.com/file/d/{file_id}/view"
        print(f"  Uploaded: {filename}")
        print(f"    {url}")
        return url


def resolve_all_outputs():
    today = date.today().isoformat()
    project_root = TOOLS_DIR.parent
    candidates = [
        project_root / "outputs" / "drafts" / f"{today}-week-1.docx",
        project_root / "outputs" / "research" / f"{today}-research.xlsx",
        project_root / "outputs" / "strategy" / f"{today}-strategy.md",
    ]
    resolved = []
    for path in candidates:
        if path.exists():
            resolved.append(path)
        else:
            folder = path.parent
            if folder.exists():
                suffix = path.suffix
                matches = sorted(folder.glob(f"*{suffix}"), key=lambda p: p.stat().st_mtime, reverse=True)
                if matches:
                    resolved.append(matches[0])
    return resolved


def main():
    _check_deps()
    config = _load_config()

    args = sys.argv[1:]

    # Parse --folder-id argument (overrides config)
    folder_id = None
    if "--folder-id" in args:
        idx = args.index("--folder-id")
        if idx + 1 < len(args):
            folder_id = args[idx + 1]
            args = args[:idx] + args[idx + 2:]

    # Parse --subfolder argument (creates/finds a subfolder and uploads into it)
    subfolder = None
    if "--subfolder" in args:
        idx = args.index("--subfolder")
        if idx + 1 < len(args):
            subfolder = args[idx + 1]
            args = args[:idx] + args[idx + 2:]

    if not folder_id:
        folder_id = config.get("google_drive_folder_id", "")
    if not folder_id or folder_id in ("YOUR_FOLDER_ID_HERE", ""):
        print("Error: google_drive_folder_id not set in tools/config.json")
        print("Add your Google Drive folder ID (from the folder URL after /folders/)")
        sys.exit(0)

    if not args:
        print("Usage: python tools/upload_gdrive.py <file> [file ...]")
        print("       python tools/upload_gdrive.py --all")
        print("       python tools/upload_gdrive.py --all --folder-id <id>")
        sys.exit(0)

    if args == ["--all"]:
        files = resolve_all_outputs()
        if not files:
            print("No output files found to upload.")
            sys.exit(0)
    else:
        files = [Path(a) for a in args]

    service = _get_service()

    if subfolder:
        folder_id = create_or_find_folder(service, subfolder, folder_id)

    print(f"Uploading {len(files)} file(s) to Google Drive...")

    for f in files:
        upload_file(service, f, folder_id)

    print("Done.")


if __name__ == "__main__":
    main()
