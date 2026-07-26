"""Status vocabularies, lane definitions, and the CSV schema.

Three *separate* status vocabularies exist in this repo and must never be
cross-contaminated (see the plan's integration constraints):

- ``SEEN_STATUSES``  -> ``job_scraper/seen_jobs.json`` ``status`` field
- ``CSV_STATUSES``   -> ``job_search_tracker.csv`` ``status`` column
- (``outcome.md`` has a third vocabulary the tracker never writes)
"""

# --- job_search_tracker.csv -------------------------------------------------

# Exact 13-column header, in order. Any deviation on disk is a hard error:
# /scrape, /rank, and /outcome all depend on this schema.
CSV_HEADER = [
    "date", "company", "sector", "role", "role_type", "channel", "status",
    "contact_person", "fit_rating", "notes", "cv_file", "cover_letter_file", "source",
]

# CSV status column vocabulary (space-separated multi-word tokens, NOT underscores).
CSV_STATUSES = [
    "applied", "interview", "offer",
    "hired", "rejected", "no response", "withdrawn", "offer declined",
]

# Statuses that close an application (used to route to the "closed" lane).
CSV_FINAL_STATUSES = {"hired", "rejected", "no response", "withdrawn", "offer declined"}

# Statuses treated as a "win" for card styling.
CSV_WON_STATUSES = {"hired", "offer"}

# --- job_scraper/seen_jobs.json ---------------------------------------------

SEEN_STATUSES = ["new", "skipped", "evaluated", "ranked", "expired"]

# --- Board lanes ------------------------------------------------------------
# Ordered left-to-right. Each lane draws from exactly one data source.

LANES = [
    {"id": "scraped", "label": "Scraped", "source": "lead"},
    {"id": "ranked", "label": "Ranked (to apply)", "source": "lead"},
    {"id": "applied", "label": "Applied", "source": "application"},
    {"id": "interview", "label": "Interview", "source": "application"},
    {"id": "offer", "label": "Offer", "source": "application"},
    {"id": "closed", "label": "Closed", "source": "application"},
    {"id": "archived", "label": "Archived", "source": "lead"},  # expired + skipped; off by default
]


def csv_lane(status: str) -> str:
    """Map a CSV status token to its board lane id."""
    s = (status or "").strip().lower()
    if s in ("applied", "interview", "offer"):
        return s
    return "closed"


def seen_lane(status: str) -> str:
    """Map a seen_jobs status to its board lane id."""
    s = (status or "").strip().lower()
    if s == "ranked":
        return "ranked"
    if s in ("expired", "skipped"):
        return "archived"
    # new / evaluated / anything else
    return "scraped"
