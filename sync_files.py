import sys
import time
from io import TextIOWrapper
from typing import cast

from b2sdk.v2 import (
    parse_sync_folder,
    Synchronizer,
    SyncReport,
    NewerFileSyncMode,
    CompareVersionMode,
    KeepOrDeleteMode,
)


def sync_directory(b2_api, bucket_name: str, source: str, dest_prefix: str):
    dest_url = f"b2://{bucket_name}"
    if dest_prefix:
        dest_url += f"/{dest_prefix.strip('/')}"

    print(f"Syncing {source} -> {dest_url}")

    source_folder = parse_sync_folder(source, b2_api)
    dest_folder = parse_sync_folder(dest_url, b2_api)

    synchronizer = Synchronizer(
        max_workers=1,
        compare_version_mode=CompareVersionMode.MODTIME,
        newer_file_mode=NewerFileSyncMode.SKIP,
        keep_days_or_delete=KeepOrDeleteMode.NO_DELETE,
    )

    with SyncReport(cast(TextIOWrapper, sys.stdout), no_progress=False) as reporter:
        synchronizer.sync_folders(
            source_folder=source_folder,
            dest_folder=dest_folder,
            now_millis=int(round(time.time() * 1000)),
            reporter=reporter,
        )
