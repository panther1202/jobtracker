"""Build the merged, deduped board model from both data sources.

Pure read logic: combines ``job_search_tracker.csv`` (applications) and
``job_scraper/seen_jobs.json`` (scraped leads) into one funnel, dedupes leads
against applications (see ``normalize``), and attaches the "needs /outcome" flags.
Returns plain dicts so the FastAPI layer can serialize them directly.
"""

from . import normalize, pending, seen_writer
from .csv_writer import read_rows
from .models import CSV_WON_STATUSES, LANES, csv_lane, seen_lane


def _application_cards(header: list[str], rows: list[list[str]], flags: dict) -> list[dict]:
    idx = {name: header.index(name) for name in header}
    cards = []
    for i, row in enumerate(rows):
        def col(name: str) -> str:
            j = idx.get(name)
            return row[j] if j is not None and j < len(row) else ""

        status = col("status").strip().lower()
        app_id = f"app-{i}"
        cards.append({
            "id": app_id,
            "source": "application",
            "company": col("company"),
            "role": col("role"),
            "title": col("role"),
            "url": col("source") if col("source").startswith("http") else "",
            "status": status,
            "lane": csv_lane(status),
            "won": status in CSV_WON_STATUSES,
            "date": col("date"),
            "sector": col("sector"),
            "role_type": col("role_type"),
            "channel": col("channel"),
            "fit_rating": col("fit_rating"),
            "notes": col("notes"),
            "cv_file": col("cv_file"),
            "cover_letter_file": col("cover_letter_file"),
            "contact_person": col("contact_person"),
            "needs_outcome": app_id in flags,
            "pending": flags.get(app_id),
        })
    return cards


def _lead_cards(seen: dict, applications: list[dict]) -> list[dict]:
    cards = []
    for url, entry in seen.get("seen", {}).items():
        company = entry.get("company", "")
        title = entry.get("title", "")

        company_hits = [
            a for a in applications if normalize.company_matches(company, a["company"])
        ]
        exact = [a for a in company_hits if normalize.role_matches(title, a["role"])]
        if exact:
            continue  # already applied to this exact role -> hide from board

        possible_dup = None
        if company_hits:
            a = company_hits[0]
            possible_dup = {"company": a["company"], "role": a["role"]}

        status = entry.get("status", "new")
        cards.append({
            "id": url,
            "source": "lead",
            "company": company,
            "role": title,
            "title": title,
            "url": url,
            "status": status,
            "lane": seen_lane(status),
            "fit": entry.get("fit"),
            "rank_score": entry.get("rank_score"),
            "rank_verdict": entry.get("rank_verdict"),
            "rank_date": entry.get("rank_date"),
            "location_flag": entry.get("location_flag"),
            "possible_duplicate": possible_dup,
        })
    # Ranked leads sorted by score desc (highest-priority "to apply" first).
    cards.sort(key=lambda c: (c.get("rank_score") or -1), reverse=True)
    return cards


def build_board() -> dict:
    """Assemble the full board: lane metadata, cards grouped by lane, and summary."""
    header, rows = read_rows()
    flags = pending.read()
    applications = _application_cards(header, rows, flags)
    leads = _lead_cards(seen_writer.read_seen(), applications)

    by_lane: dict[str, list[dict]] = {lane["id"]: [] for lane in LANES}
    for card in applications + leads:
        by_lane.setdefault(card["lane"], []).append(card)

    summary = {
        "remaining_to_apply": len(by_lane.get("ranked", [])),
        "awaiting_response": len(by_lane.get("applied", [])),
        "in_interview": len(by_lane.get("interview", [])),
        "offers": len(by_lane.get("offer", [])),
        "closed": len(by_lane.get("closed", [])),
        "needs_outcome": sum(1 for a in applications if a["needs_outcome"]),
    }

    return {
        "lanes": [
            {**lane, "count": len(by_lane.get(lane["id"], [])), "cards": by_lane.get(lane["id"], [])}
            for lane in LANES
        ],
        "summary": summary,
    }
