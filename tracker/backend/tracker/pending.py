"""Sidecar tracking which applications were edited in-app and still need /outcome.

The CSV schema is frozen (13 columns) so we cannot add a column, and diffing
``outcome.md`` is fragile (its status vocabulary differs). Instead we keep a small
git-ignored sidecar ``tracker/pending_outcomes.json`` keyed by application id:

    {"app-2": {"company": "CNN", "role": "...", "changed": "status", "ts": "..."}}

A flagged card renders a "changed in app - run /outcome <company>" badge. The user
dismisses it (per card) after running /outcome to archive + calibrate.
"""

import json
from datetime import datetime, timezone

from . import paths


def read() -> dict:
    path = paths.pending_file()
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write(data: dict) -> None:
    path = paths.pending_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def flag(app_id: str, *, company: str, role: str, changed: str) -> None:
    """Record that ``app_id`` was edited in-app and needs /outcome."""
    data = read()
    data[app_id] = {
        "company": company,
        "role": role,
        "changed": changed,
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    _write(data)


def dismiss(app_id: str) -> bool:
    """Clear the flag for ``app_id``. Returns True if a flag was removed."""
    data = read()
    if app_id in data:
        del data[app_id]
        _write(data)
        return True
    return False
