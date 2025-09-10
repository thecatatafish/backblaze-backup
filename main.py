import os
import uuid
from datetime import datetime
from pathlib import Path
from b2sdk.v2 import InMemoryAccountInfo, B2Api

APPLICATION_KEY_ID = os.environ["APPLICATION_KEY_ID"]
APPLICATION_KEY = os.environ["APPLICATION_KEY"]
BUCKET_NAME = os.environ["BUCKET_NAME"]
SOURCE_DIR = "./data"



info = InMemoryAccountInfo()
b2_api = B2Api(info)
b2_api.authorize_account("production", APPLICATION_KEY_ID, APPLICATION_KEY)
bucket = b2_api.get_bucket_by_name(BUCKET_NAME)

# Generate backup directory prefix
backup_prefix = datetime.today().strftime('%Y-%m-%d') + '-' + str(uuid.uuid4())[:8]

def upload_file(local_path: Path, remote_path: str):
    with local_path.open('rb') as file:
        bucket.upload_bytes(file.read(), remote_path)

def backup_directory(source: str):
    base_path = Path(source).resolve()
    for root, _, files in os.walk(base_path):
        for filename in files:
            local_file = Path(root) / filename
            relative_path = local_file.relative_to(base_path)
            remote_file = f"{backup_prefix}/{str(relative_path)}"
            print(f"Uploading {local_file} -> {remote_file}")
            upload_file(local_file, remote_file)

if __name__ == "__main__":
    print("Starting backup...")
    backup_directory(SOURCE_DIR)
