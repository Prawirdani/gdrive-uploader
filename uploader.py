import os
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from config import load_config


def upload_to_drive(cfg_path: str, file_path: str):
    cfg = load_config(cfg_path)
    creds = Credentials(
        None,
        refresh_token=cfg.refresh_token,
        client_id=cfg.client_id,
        client_secret=cfg.client_secret,
        scopes=cfg.scopes,
        token_uri="https://oauth2.googleapis.com/token",
    )

    service = build("drive", "v3", credentials=creds)

    # --------------------------
    # Helper: create folder
    # --------------------------
    def create_folder(name, parent_id=None):
        """Create a folder in Google Drive and return its ID."""
        metadata = {"name": name, "mimeType": "application/vnd.google-apps.folder"}
        if parent_id:
            metadata["parents"] = [parent_id]

        folder = service.files().create(body=metadata, fields="id").execute()
        print(f"📁 Created folder: {name} (ID: {folder.get('id')})")
        return folder.get("id")

    # --------------------------
    # Helper: upload a single file
    # --------------------------
    def upload_file(filepath, parent_id=None):
        """Upload a single file to Google Drive."""
        file_metadata = {"name": os.path.basename(filepath)}
        if parent_id:
            file_metadata["parents"] = [parent_id]

        media = MediaFileUpload(filepath, resumable=True)
        uploaded_file = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id, name")
            .execute()
        )
        print(
            f"✅ Uploaded: {uploaded_file.get('name')} (ID: {uploaded_file.get('id')})"
        )

    # --------------------------
    # Helper: upload a folder recursively
    # --------------------------
    def upload_folder(local_folder, parent_id=None):
        """Recursively upload a local folder and its contents."""
        folder_name = os.path.basename(local_folder.rstrip("/"))
        folder_id = create_folder(folder_name, parent_id)

        for entry in os.scandir(local_folder):
            if entry.is_file():
                upload_file(entry.path, folder_id)
            elif entry.is_dir():
                upload_folder(entry.path, folder_id)

    # --------------------------
    # Main upload logic
    # --------------------------
    if not os.path.exists(file_path):
        print(f"❌ Error: path not found: {file_path}")
        sys.exit(1)

    if os.path.isdir(file_path):
        print(f"📂 Uploading folder: {file_path}")
        upload_folder(file_path, cfg.folder_id)
    else:
        upload_file(file_path, cfg.folder_id)
