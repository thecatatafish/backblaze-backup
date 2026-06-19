import os
import tomllib
from dataclasses import dataclass
from pathlib import Path

SNAPSHOT = "snapshot"
SYNC = "sync"
JOB_TYPES = (SNAPSHOT, SYNC)


class Config:
    APPLICATION_KEY_ID = os.environ["APPLICATION_KEY_ID"]
    APPLICATION_KEY = os.environ["APPLICATION_KEY"]
    BUCKET_NAME = os.environ["BUCKET_NAME"]


@dataclass
class Job:
    name: str
    type: str
    source: str
    dest_prefix: str


def load_jobs(config_path: str = "jobs.toml") -> list[Job]:
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("rb") as f:
        data = tomllib.load(f)

    raw_jobs = data.get("jobs", [])
    if not raw_jobs:
        raise ValueError(f"No jobs defined in {path}")

    jobs = []
    for i, raw in enumerate(raw_jobs):
        for field in ("name", "type", "source", "dest_prefix"):
            if field not in raw:
                raise ValueError(f"Job #{i + 1} in {path} is missing required field '{field}'")
        if raw["type"] not in JOB_TYPES:
            raise ValueError(
                f"Job '{raw['name']}' has invalid type '{raw['type']}'; "
                f"must be one of {JOB_TYPES}"
            )
        jobs.append(
            Job(
                name=raw["name"],
                type=raw["type"],
                source=raw["source"],
                dest_prefix=raw["dest_prefix"],
            )
        )
    return jobs
