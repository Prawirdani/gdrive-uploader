import sys
from uploader import upload_to_drive

CONFIG_FILE = "config.json"  # Change this if you rename the default config file name (config.json)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: upload_to_drive.py <file_path>")
        sys.exit(1)
    # TODO: Check config.json
    upload_to_drive(CONFIG_FILE, sys.argv[1])
