import uuid
from datetime import datetime
from pathlib import Path


def upload_file(bucket, local_path: Path, remote_path: str):
    with local_path.open("rb") as file:
        bucket.upload_bytes(file.read(), remote_path)


def snapshot_file(bucket, source: str, dest_prefix: str):
    backup_prefix = datetime.today().strftime("%Y-%m-%d") + "-" + str(uuid.uuid4())[:8]
    base_path = Path(source)

    remote_file = f"{dest_prefix.strip('/')}/{backup_prefix}/{base_path.name}"
    print(f"Uploading {base_path} -> {remote_file}")
    upload_file(bucket, base_path, remote_file)
