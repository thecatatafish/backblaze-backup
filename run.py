from b2sdk.v2 import InMemoryAccountInfo, B2Api

from config import Config, Job, SNAPSHOT, SYNC, load_jobs
from snapshot_file import snapshot_file
from sync_files import sync_directory


def build_b2_api() -> B2Api:
    info = InMemoryAccountInfo()
    b2_api = B2Api(info)
    b2_api.authorize_account("production", Config.APPLICATION_KEY_ID, Config.APPLICATION_KEY)
    return b2_api


def run_job(b2_api: B2Api, job: Job):
    print(f"\n=== Job '{job.name}' ({job.type}) ===")
    if job.type == SNAPSHOT:
        bucket = b2_api.get_bucket_by_name(Config.BUCKET_NAME)
        snapshot_file(bucket, job.source, job.dest_prefix)
    elif job.type == SYNC:
        sync_directory(b2_api, Config.BUCKET_NAME, job.source, job.dest_prefix)
    print(f"=== Job '{job.name}' complete ===")


def main():
    jobs = load_jobs()
    b2_api = build_b2_api()
    for job in jobs:
        run_job(b2_api, job)
    print("\nAll jobs complete.")


if __name__ == "__main__":
    main()
