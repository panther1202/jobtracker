"""Tests for the tracker write paths: CSV row updates, seen_jobs status, sidecar.

These never touch the real (git-ignored) data files: every test points the
AIJS_* env overrides at temp fixtures.
"""

import csv
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

# The importable package lives at tracker/backend/tracker; put tracker/backend on
# the path first so the regular package wins over the bare top-level tracker/ dir.
_BACKEND = Path(__file__).resolve().parents[1] / "tracker" / "backend"
sys.path.insert(0, str(_BACKEND))

from tracker import csv_writer, pending, seen_writer  # noqa: E402
from tracker.csv_writer import SchemaError  # noqa: E402
from tracker.models import CSV_HEADER  # noqa: E402

_HEADER_LINE = ",".join(CSV_HEADER)

# A row whose notes field contains commas, to prove quoting survives a rewrite.
_ROW_A = (
    "2026-07-13,Morgan Stanley,Finance/Tech,AI / ML Engineer,AI Engineer,LinkedIn,"
    'applied,,78,"Strong fit; LangChain, Bedrock map 1:1",cv/a.pdf,cl/a.pdf,LinkedIn'
)
_ROW_B = (
    "2026-07-13,CNN,Media,Machine Learning Engineer I,ML Engineer,LinkedIn,"
    'applied,,75,"Recsys is a gap",cv/b.pdf,cl/b.pdf,LinkedIn'
)


class _TempDataCase(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        base = Path(self.dir.name)
        self.csv_path = base / "job_search_tracker.csv"
        self.seen_path = base / "seen_jobs.json"
        self.pending_path = base / "pending.json"
        os.environ["AIJS_TRACKER_CSV"] = str(self.csv_path)
        os.environ["AIJS_SEEN_JOBS"] = str(self.seen_path)
        os.environ["AIJS_PENDING"] = str(self.pending_path)

    def tearDown(self):
        for k in ("AIJS_TRACKER_CSV", "AIJS_SEEN_JOBS", "AIJS_PENDING"):
            os.environ.pop(k, None)
        self.dir.cleanup()

    def write_csv(self, *rows):
        self.csv_path.write_text("\n".join([_HEADER_LINE, *rows]) + "\n", encoding="utf-8")

    def read_csv_rows(self):
        with open(self.csv_path, "r", encoding="utf-8", newline="") as f:
            return [r for r in csv.reader(f) if r]


class CsvWriterTests(_TempDataCase):
    def test_update_status_preserves_header_and_other_rows(self):
        self.write_csv(_ROW_A, _ROW_B)
        csv_writer.update_row(0, status="interview")
        rows = self.read_csv_rows()
        self.assertEqual(rows[0], CSV_HEADER)          # header intact & in order
        self.assertEqual(len(rows), 3)                 # header + 2 data rows, none dropped
        self.assertEqual(rows[1][CSV_HEADER.index("status")], "interview")
        self.assertEqual(rows[2][CSV_HEADER.index("status")], "applied")  # row B untouched

    def test_notes_with_commas_stay_intact_and_quoted(self):
        self.write_csv(_ROW_A)
        csv_writer.update_row(0, status="offer")
        # Re-parsed value keeps the embedded commas as one field.
        rows = self.read_csv_rows()
        self.assertEqual(rows[1][CSV_HEADER.index("notes")], "Strong fit; LangChain, Bedrock map 1:1")
        # And the raw file still quotes it.
        self.assertIn('"Strong fit; LangChain, Bedrock map 1:1"', self.csv_path.read_text(encoding="utf-8"))

    def test_update_notes_only(self):
        self.write_csv(_ROW_A)
        csv_writer.update_row(0, notes="called back 2026-07-20")
        rows = self.read_csv_rows()
        self.assertEqual(rows[1][CSV_HEADER.index("notes")], "called back 2026-07-20")
        self.assertEqual(rows[1][CSV_HEADER.index("status")], "applied")  # unchanged

    def test_invalid_status_rejected(self):
        self.write_csv(_ROW_A)
        with self.assertRaises(ValueError):
            csv_writer.update_row(0, status="in_progress")  # outcome.md vocab, not CSV vocab

    def test_index_out_of_range(self):
        self.write_csv(_ROW_A)
        with self.assertRaises(IndexError):
            csv_writer.update_row(5, status="offer")

    def test_bad_header_refuses_write(self):
        self.csv_path.write_text("wrong,header\n1,2\n", encoding="utf-8")
        with self.assertRaises(SchemaError):
            csv_writer.update_row(0, status="offer")


class SeenWriterTests(_TempDataCase):
    def _seed(self):
        doc = {"seen": {
            "http://x/1": {"title": "AI Engineer", "company": "Eightpoint", "url": "http://x/1",
                            "first_seen": "2026-07-13", "fit": "high", "status": "ranked",
                            "rank_score": 80, "rank_verdict": "Strong Fit", "rank_date": "2026-07-13"},
        }}
        self.seen_path.write_text(json.dumps(doc), encoding="utf-8")

    def test_update_status_keeps_rank_fields(self):
        self._seed()
        entry = seen_writer.update_status("http://x/1", "skipped")
        self.assertEqual(entry["status"], "skipped")
        on_disk = json.loads(self.seen_path.read_text(encoding="utf-8"))["seen"]["http://x/1"]
        self.assertEqual(on_disk["status"], "skipped")
        # Additive /rank fields must survive untouched.
        self.assertEqual(on_disk["rank_score"], 80)
        self.assertEqual(on_disk["rank_verdict"], "Strong Fit")
        self.assertEqual(on_disk["fit"], "high")

    def test_invalid_status_rejected(self):
        self._seed()
        with self.assertRaises(ValueError):
            seen_writer.update_status("http://x/1", "applied")  # CSV vocab, not seen vocab

    def test_unknown_url_raises(self):
        self._seed()
        with self.assertRaises(KeyError):
            seen_writer.update_status("http://x/missing", "skipped")


class PendingTests(_TempDataCase):
    def test_flag_and_dismiss_round_trip(self):
        self.assertEqual(pending.read(), {})
        pending.flag("app-0", company="CNN", role="ML Engineer I", changed="status")
        data = pending.read()
        self.assertIn("app-0", data)
        self.assertEqual(data["app-0"]["company"], "CNN")
        self.assertTrue(pending.dismiss("app-0"))
        self.assertEqual(pending.read(), {})
        self.assertFalse(pending.dismiss("app-0"))  # idempotent


if __name__ == "__main__":
    unittest.main()
