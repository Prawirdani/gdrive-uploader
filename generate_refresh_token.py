import json
import sys
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
OUT = "config.json"


def main(creds_filename: str):
    # Run OAuth flow
    flow = InstalledAppFlow.from_client_secrets_file(creds_filename, SCOPES)
    creds = flow.run_local_server(port=0)

    # Extract client info from the credentials file
    with open(creds_filename, "r") as f:
        client_data = json.load(f)["installed"]
        client_id = client_data["client_id"]
        client_secret = client_data["client_secret"]

    # Build config structure
    config = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": creds.refresh_token,
        "scopes": SCOPES,
        "folder_id": "",
    }

    # Write to config.json
    with open(OUT, "w") as f:
        json.dump(config, f, indent=4)

    print(f"✅ Successfully generated config file: {OUT}")
    print("🔁 Refresh Token:", creds.refresh_token)
    print("💾 You can now use this config.json directly with main.py")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: generate_refresh_token.py <credentials>.json")
        sys.exit(1)

    creds_file = sys.argv[1]
    main(creds_file)
