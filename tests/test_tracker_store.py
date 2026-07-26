"""Tests for board assembly and lead/application dedup."""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

_BACKEND = Path(__file__).resolve().parents[1] / "tracker" / "backend"
sys.path.insert(0, str(_BACKEND))

from tracker import normalize, store  # noqa: E402
from tracker.models import CSV_HEADER  # noqa: E402

_HEADER_LINE = ",".join(CSV_HEADER)


class NormalizeTests(unittest.TestCase):
    def test_company_match_ignores_parentheticals_and_suffixes(self):
        self.assertTrue(normalize.company_matches("CNN", "CNN (NYC)"))
        self.assertTrue(normalize.company_matches("NYU Langone", "NYU Langone Health"))
        self.assertTrue(normalize.company_matches("Tessera Labs", "Tessera Labs"))
        self.assertFalse(normalize.company_matches("Notion", "Nuro"))

    def test_role_match_is_exact_on_tokens(self):
        self.assertTrue(normalize.role_matches("AI / ML Engineer", "AI / ML Engineer"))
        # The Notion trap: one extra token must NOT collapse two distinct roles.
        self.assertFalse(normalize.role_matches(
            "Software Engineer, Early Career (AI)", "Software Engineer, Early Career"))


class BoardTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        base = Path(self.dir.name)
        self.csv_path = base / "tracker.csv"
        self.seen_path = base / "seen.json"
        os.environ["AIJS_TRACKER_CSV"] = str(self.csv_path)
        os.environ["AIJS_SEEN_JOBS"] = str(self.seen_path)
        os.environ["AIJS_PENDING"] = str(base / "pending.json")

        # One application: applied to Notion "Early Career (AI)".
        row = ("2026-07-13,Notion,Software,\"Software Engineer, Early Career (AI)\",AI Engineer,"
               "LinkedIn,applied,,74,notes here,cv/n.pdf,cl/n.pdf,LinkedIn")
        self.csv_path.write_text(_HEADER_LINE + "\n" + row + "\n", encoding="utf-8")

        seen = {"seen": {
            # Exact same role at Notion -> should be HIDDEN (already applied).
            "http://j/notion-ai": {"title": "Software Engineer, Early Career (AI)", "company": "Notion",
                                    "url": "http://j/notion-ai", "first_seen": "2026-07-13",
                                    "fit": "high", "status": "ranked", "rank_score": 74},
            # Different Notion role -> SHOWN, tagged possible_duplicate.
            "http://j/notion-ec": {"title": "Software Engineer, Early Career", "company": "Notion",
                                    "url": "http://j/notion-ec", "first_seen": "2026-07-13",
                                    "fit": "medium", "status": "ranked", "rank_score": 61},
            # Unrelated ranked lead, higher score -> should sort first in Ranked lane.
            "http://j/ms": {"title": "AI / ML Engineer", "company": "Morgan Stanley",
                             "url": "http://j/ms", "first_seen": "2026-07-13", "fit": "medium",
                             "status": "ranked", "rank_score": 78},
            # Expired lead -> Archived lane.
            "http://j/old": {"title": "AI/ML Developer", "company": "Calpion", "url": "http://j/old",
                              "first_seen": "2026-07-13", "fit": "high", "status": "expired"},
        }}
        self.seen_path.write_text(json.dumps(seen), encoding="utf-8")

    def tearDown(self):
        for k in ("AIJS_TRACKER_CSV", "AIJS_SEEN_JOBS", "AIJS_PENDING"):
            os.environ.pop(k, None)
        self.dir.cleanup()

    def _lane(self, board, lane_id):
        return next(l for l in board["lanes"] if l["id"] == lane_id)

    def test_exact_role_match_is_hidden(self):
        board = store.build_board()
        ranked_urls = {c["url"] for c in self._lane(board, "ranked")["cards"]}
        self.assertNotIn("http://j/notion-ai", ranked_urls)

    def test_company_only_match_is_shown_with_duplicate_hint(self):
        board = store.build_board()
        ec = next(c for c in self._lane(board, "ranked")["cards"] if c["url"] == "http://j/notion-ec")
        self.assertIsNotNone(ec["possible_duplicate"])
        self.assertEqual(ec["possible_duplicate"]["company"], "Notion")

    def test_ranked_sorted_by_score_desc(self):
        board = store.build_board()
        scores = [c["rank_score"] for c in self._lane(board, "ranked")["cards"]]
        self.assertEqual(scores, sorted(scores, reverse=True))
        self.assertEqual(self._lane(board, "ranked")["cards"][0]["url"], "http://j/ms")

    def test_application_lands_in_applied_lane(self):
        board = store.build_board()
        applied = self._lane(board, "applied")["cards"]
        self.assertEqual(len(applied), 1)
        self.assertEqual(applied[0]["company"], "Notion")
        self.assertEqual(applied[0]["id"], "app-0")

    def test_expired_goes_to_archived(self):
        board = store.build_board()
        archived_urls = {c["url"] for c in self._lane(board, "archived")["cards"]}
        self.assertIn("http://j/old", archived_urls)

    def test_summary_counts(self):
        board = store.build_board()
        self.assertEqual(board["summary"]["awaiting_response"], 1)
        self.assertEqual(board["summary"]["remaining_to_apply"], 2)  # notion-ec + ms


if __name__ == "__main__":
    unittest.main()
