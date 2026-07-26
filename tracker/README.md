# Job Tracker App

A local, interactive board over your job-search pipeline. It reads the two data
files the Claude commands already maintain and shows the full funnel in one view:

```
Scraped → Ranked (to apply) → Applied → Interview → Offer → Closed      [+ Archived]
└──────── job_scraper/seen_jobs.json ─────┘ └──────── job_search_tracker.csv ────────┘
```

- **Ranked** is your "what's remaining" queue — scraped jobs `/rank` scored but you
  have not applied to yet, sorted by score.
- **Applied → Closed** are your real applications from the tracker CSV.
- Click a card to expand it: change status, edit notes, open the posting.
- Drag an application card between **Applied / Interview / Offer** to update its status.
  (Move to a *Closed* status — hired, rejected, etc. — with the card's status dropdown,
  since "closed" maps to several outcomes.)

## How it stays in sync with the automation

The app is a **view + light editor**, not a replacement for the commands:

| You do this in the app | It writes | You still run in Claude |
|---|---|---|
| Change an application's status / notes | `job_search_tracker.csv` (that row only) | `/outcome <company>` — archives the posting + `outcome.md` so `/setup` can calibrate fit scoring |
| Change a scraped lead's status (e.g. dismiss to `skipped`) | `job_scraper/seen_jobs.json` (that entry's `status` only) | — |
| — apply to a ranked lead — | (nothing) | `/apply <url>` then `/outcome` |

Because the app can't fetch postings or run calibration, any application you edit in
the app gets a **"needs /outcome"** badge (tracked in the git-ignored
`tracker/pending_outcomes.json`). Run `/outcome <company>` in Claude, then dismiss the
badge. The app never touches `outcome.md` or the profile/evaluation files.

**Dedup caveat.** A ranked lead is hidden once you've applied to that exact
company+role. Leads at a company you applied to under a *different* title (e.g. NYU
Langone "Machine Learning Engineer" vs. your applied "Engineer II, Applied AI") stay
visible with a soft "possible duplicate" hint — dismiss them with the status dropdown
if they're the same job. Perfect automatic dedup isn't possible; the hint + dismiss is
the escape hatch.

## Running it

Two processes in dev (frontend hot-reload proxies `/api` to the backend):

```bash
# 1. Backend (FastAPI) — from tracker/backend/
pip install -r requirements.txt
uvicorn app:app --reload --port 8100

# 2. Frontend (Vite + React, run with Bun) — from tracker/frontend/
bun install
bun run dev        # opens http://localhost:5173
```

Single-process (no hot reload): build the frontend once and let FastAPI serve it.

```bash
cd tracker/frontend && bun run build      # emits tracker/frontend/dist/
cd ../backend && uvicorn app:app --port 8100
# open http://127.0.0.1:8100
```

## Tests

- Backend logic: `python -m unittest discover -s tests -t .` (from repo root) —
  `tests/test_tracker_store.py`, `tests/test_tracker_writers.py`. Stdlib `unittest`,
  fixture copies only; the real data files are never touched.
- Frontend types: `bun run typecheck` (from `tracker/frontend/`).

## Layout

```
tracker/
  backend/
    tracker/        pure logic (stdlib only): paths, models, normalize, store, *_writer, pending
    app.py          FastAPI routes; serves frontend/dist in production
    requirements.txt
  frontend/         React + TypeScript + Vite (Bun-run)
```

All data lives in the repo-root files, not here — this directory is just the app.
