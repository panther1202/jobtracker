"""FastAPI HTTP layer over the tracker package.

Thin: every route delegates to the pure logic in ``tracker/`` and returns the
freshly-rebuilt board so the frontend always renders authoritative state. Reads
happen on every request (files are tiny) so edits made by Claude commands
(/scrape, /rank, /outcome) show up without a restart.

Run (dev):   uvicorn app:app --reload --port 8100   (from tracker/backend/)
Serves the built frontend at / when tracker/frontend/dist exists.
"""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from tracker import csv_writer, pending, seen_writer, store
from tracker.csv_writer import SchemaError

app = FastAPI(title="Job Tracker", version="1.0.0")

# Dev-only: Vite dev server runs on a different port and proxies /api, but allow
# direct cross-origin calls too for convenience on localhost.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ApplicationPatch(BaseModel):
    id: str
    status: str | None = None
    notes: str | None = None


class LeadPatch(BaseModel):
    url: str
    status: str


class DismissBody(BaseModel):
    id: str


def _parse_app_index(app_id: str) -> int:
    if not app_id.startswith("app-"):
        raise HTTPException(status_code=422, detail=f"Bad application id {app_id!r}")
    try:
        return int(app_id[len("app-"):])
    except ValueError:
        raise HTTPException(status_code=422, detail=f"Bad application id {app_id!r}")


@app.get("/api/board")
def get_board():
    try:
        return store.build_board()
    except SchemaError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.patch("/api/application")
def patch_application(body: ApplicationPatch):
    if body.status is None and body.notes is None:
        raise HTTPException(status_code=422, detail="Nothing to update")
    index = _parse_app_index(body.id)
    try:
        row = csv_writer.update_row(index, status=body.status, notes=body.notes)
    except (ValueError, IndexError) as e:
        raise HTTPException(status_code=422, detail=str(e))
    except SchemaError as e:
        raise HTTPException(status_code=500, detail=str(e))

    header, _ = csv_writer.read_rows()
    company = row[header.index("company")]
    role = row[header.index("role")]
    changed = "status" if body.status is not None else "notes"
    if body.status is not None and body.notes is not None:
        changed = "status+notes"
    pending.flag(body.id, company=company, role=role, changed=changed)
    return store.build_board()


@app.patch("/api/lead")
def patch_lead(body: LeadPatch):
    try:
        seen_writer.update_status(body.url, body.status)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return store.build_board()


@app.post("/api/pending/dismiss")
def dismiss_pending(body: DismissBody):
    pending.dismiss(body.id)
    return store.build_board()


# --- Serve the built frontend (single-process production run) ---------------
_DIST = Path(__file__).parent.parent / "frontend" / "dist"
if _DIST.is_dir():
    app.mount("/", StaticFiles(directory=str(_DIST), html=True), name="frontend")
