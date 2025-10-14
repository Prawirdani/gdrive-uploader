# ☁️ Google Drive Uploader (Python)

A lightweight Python tool to **upload files or folders to Google Drive** using OAuth2 with a persistent refresh token.  
Once authorized, it can run headlessly perfect for backups or automated uploads.

## 🧰 Requirements

- Python 3.8+
- Google Drive API OAuth credentials
- Internet access


## ⚙️ Installation

1. Clone or download this repository.
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```


##  1. Set up Google OAuth credentials 🔑

Before using the uploader, you need a pair of OAuth **Client ID** and **Client Secret** from Google Cloud.

To make this process easier, follow the clear step-by-step guide here:  
👉 **[rclone.org/drive/#making-your-own-client-id](https://rclone.org/drive/#making-your-own-client-id)**

That guide walks you through:
- Enabling the Google Drive API  
- Creating OAuth 2.0 credentials  
- Downloading your `client_secret_*.json` file  

Save that JSON file you’ll use it in the next step to generate your refresh token.


## 2. Generate your config.json *(one-time)* ⚙️

> ⚠️ Run this **once on a machine with a web browser**, since it opens a local authorization page.

This step will:

* Launch a short browser-based OAuth prompt
* Retrieve your access + refresh tokens
* Automatically generate a ready-to-use `config.json`

```bash
python generate_refresh_token.py client_secret_xxxx.json
```

Example output:

```
✅ Successfully generated config file: config.json
🔁 Refresh Token: 1//0abcdEfGHiJklMnOpQrStuVwxyz
💾 You can now use this config.json directly with main.py
```

You only need to do this once.
Afterwards, keep your config.json safe it contains your credentials and refresh token.
If you plan to run uploads on a headless or remote machine **e.g., VPS**, simply copy this config.json there no need to redo the authentication process.


##  3. (Optional) Set a default Drive folder 📁 
By default, files and folders are uploaded to your Google Drive root directory.
You can optionally configure a default upload folder by editing your generated config.json and setting the folder_id field.

```json
{
  "client_id": "your_client_id",
  "client_secret": "your_client_secret",
  "refresh_token": "your_refresh_token",
  "scopes": ["https://www.googleapis.com/auth/drive.file"],
  "folder_id": "optional_drive_folder_id"
}
````
You can find the folder ID in your Drive folder URL:
```bash
https://drive.google.com/drive/folders/1A2B3CxyzDEF45
                                         ↑ this part
```
Leave it as an empty string ("") to upload directly to your Drive root.


##  4. Upload files or folders 📤

### Upload a single file

```bash
python main.py /path/to/file.txt
```

### Upload a folder (recursive)

```bash
python main.py /path/to/folder/
```

The uploader will:

* Create corresponding folders in Drive
* Upload all files inside
* Print the uploaded Drive file IDs

Example output:

```
📂 Uploading folder: /path/to/folder
✅ Uploaded: backup.sql.gz (ID: 1AbCxyz...)
📁 Created folder: logs (ID: 2QwErt...)
✅ Uploaded: access.log (ID: 2QwErt-abc123)
```


## 🖥️ Using on a Headless or Remote Machine

If you plan to use this uploader on a **headless server** (for example, a VPS or remote environment without a browser),  
you’ll need to use **two machines** during initial setup:

1. **Machine A (with a web browser)**  
  - Install this project and its dependencies (`pip install -r requirements.txt`).  
  - Run `generate_refresh_token.py` using your downloaded `client_secret_*.json`.  
  - Complete the sign-in flow in your browser this creates a `config.json` containing your credentials and refresh token.
2. **Machine B (headless / remote)**  
  - Also install this project and its dependencies.  
  - Copy the generated `config.json` from Machine A to this environment.  
  - You can now run uploads here freely no browser or re-authentication needed.

You only need to repeat the authentication step (on Machine A) if your refresh token becomes invalid or revoked.


## Notes
- **Keep `config.json` safe** it contains your client credentials and refresh token. Treat it like a password.  
- **Use descriptive folder names** in Drive to avoid confusion when uploading multiple backups.  
- **Check folder ID carefully** copying the wrong ID will upload files to an unintended location.  
- **Avoid large simultaneous uploads** split huge folders if necessary to prevent API errors.  
- **Reusing config.json** once generated, you can reuse it across machines (headless or local) without re-authentication.  
- **Refresh token expiration** if uploads fail due to an invalid token, rerun `generate_refresh_token.py` on a machine with a browser to generate a new token.  
- **Automation** you can wrap `main.py` in scripts or cron jobs for scheduled uploads.  
- **Folder structure** the uploader preserves local folder hierarchy when uploading recursively.  
- **Dependencies** make sure both machines have the project installed with `pip install -r requirements.txt`.  

