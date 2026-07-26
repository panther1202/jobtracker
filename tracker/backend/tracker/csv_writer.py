"""Read and safely mutate ``job_search_tracker.csv``.

Hard rules (the CSV is shared with /scrape, /rank, /outcome):
- Preserve the exact 13-column header and column order.
- Read-modify-write only the matched row's ``status`` / ``notes`` cells.
- Never reorder, drop, or add rows or columns.
- Quote the ``notes`` field (csv QUOTE_MINIMAL reproduces the original quoting).
"""

import csv

from . import paths
from .models import CSV_HEADER, CSV_STATUSES


class SchemaError(RuntimeError):
    """Raised when the CSV header does not match the expected 13-column schema."""


def read_rows() -> tuple[list[str], list[list[str]]]:
    """Return ``(header, rows)`` from the tracker CSV. Missing file -> canonical empty."""
    path = paths.tracker_csv()
    if not path.exists():
        return list(CSV_HEADER), []
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        all_rows = [r for r in reader if r]  # skip blank trailing lines
    if not all_rows:
        return list(CSV_HEADER), []
    header = all_rows[0]
    if header != CSV_HEADER:
        raise SchemaError(
            f"Unexpected CSV header. Expected {CSV_HEADER}, found {header}. "
            "Refusing to write to avoid corrupting shared data."
        )
    return header, all_rows[1:]


def _write_rows(header: list[str], rows: list[list[str]]) -> None:
    path = paths.tracker_csv()
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


def update_row(index: int, *, status: str | None = None, notes: str | None = None) -> list[str]:
    """Update one row (0-based, excluding the header). Returns the updated row.

    Re-reads the file immediately before writing so a concurrent append by a
    Claude command is not clobbered (read-modify-write on fresh state).
    """
    if status is not None and status not in CSV_STATUSES:
        raise ValueError(f"Invalid CSV status {status!r}. Allowed: {CSV_STATUSES}")

    header, rows = read_rows()
    if not (0 <= index < len(rows)):
        raise IndexError(f"Application row {index} out of range (have {len(rows)} rows)")

    status_i = header.index("status")
    notes_i = header.index("notes")
    row = rows[index]
    if status is not None:
        row[status_i] = status
    if notes is not None:
        row[notes_i] = notes

    _write_rows(header, rows)
    return row
