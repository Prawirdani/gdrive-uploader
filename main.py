import sys
from uploader import upload_to_drive


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: upload_to_drive.py <config_file> <file_path>")
        sys.exit(1)
    # TODO: Check config.json
    upload_to_drive(sys.argv[1], sys.argv[2])
