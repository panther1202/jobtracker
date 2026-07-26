"""Read and safely mutate ``job_scraper/seen_jobs.json``.

Hard rules (shared with /scrape dedup and /rank's additive writes):
- Preserve the ``{"seen": {<url>: {...}}}`` structure.
- Mutate ONLY the ``status`` field of one entry.
- Never drop or restructure the additive /rank fields (``rank_score``,
  ``rank_verdict``, ``rank_date``, ``fit``, ``location_flag``).
"""

import json

from . import paths
from .models import SEEN_STATUSES


def read_seen() -> dict:
    """Return the parsed seen_jobs document. Missing file -> canonical empty."""
    path = paths.seen_jobs()
    if not path.exists():
        return {"seen": {}}
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict) or "seen" not in data:
        raise ValueError("seen_jobs.json missing top-level 'seen' key")
    return data


def update_status(url: str, status: str) -> dict:
    """Set one entry's ``status``. Returns the updated entry. Read-modify-write."""
    if status not in SEEN_STATUSES:
        raise ValueError(f"Invalid seen_jobs status {status!r}. Allowed: {SEEN_STATUSES}")

    data = read_seen()
    entry = data["seen"].get(url)
    if entry is None:
        raise KeyError(f"No seen_jobs entry for url {url!r}")
    entry["status"] = status  # mutate only this field; all other keys untouched

    path = paths.seen_jobs()
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return entry
