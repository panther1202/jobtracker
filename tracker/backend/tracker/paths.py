"""Resolve the repo-root data files the tracker reads and writes.

All paths are exposed as *functions* (not module constants) so tests can point
them at fixture copies via environment variables without touching the real,
git-ignored personal data files:

- ``AIJS_ROOT``         overrides the repo-root directory
- ``AIJS_TRACKER_CSV``  overrides the applications CSV
- ``AIJS_SEEN_JOBS``    overrides the scraped-jobs JSON
- ``AIJS_PENDING``      overrides the "needs /outcome" sidecar
"""

import os
from pathlib import Path

# tracker/backend/tracker/paths.py -> parents[3] == repo root
_REPO_ROOT_DEFAULT = Path(__file__).resolve().parents[3]


def repo_root() -> Path:
    return Path(os.environ.get("AIJS_ROOT", _REPO_ROOT_DEFAULT))


def tracker_csv() -> Path:
    return Path(os.environ.get("AIJS_TRACKER_CSV", repo_root() / "job_search_tracker.csv"))


def seen_jobs() -> Path:
    return Path(os.environ.get("AIJS_SEEN_JOBS", repo_root() / "job_scraper" / "seen_jobs.json"))


def pending_file() -> Path:
    return Path(os.environ.get("AIJS_PENDING", repo_root() / "tracker" / "pending_outcomes.json"))
