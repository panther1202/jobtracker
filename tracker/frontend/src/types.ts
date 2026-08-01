// Mirrors the card/board dicts produced by tracker/backend/tracker/store.py.

export interface PendingInfo {
  company: string;
  role: string;
  changed: string;
  ts: string;
}

export interface Card {
  id: string;
  source: "application" | "lead";
  company: string;
  role: string;
  title: string;
  url: string;
  status: string;
  lane: string;

  // application-only
  won?: boolean;
  date?: string;
  sector?: string;
  role_type?: string;
  channel?: string;
  fit_rating?: string;
  notes?: string;
  cv_file?: string;
  cover_letter_file?: string;
  contact_person?: string;
  needs_outcome?: boolean;
  pending?: PendingInfo | null;

  // lead-only
  fit?: string | null;
  rank_score?: number | null;
  rank_verdict?: string | null;
  rank_date?: string | null;
  location_flag?: string | null;
  possible_duplicate?: { company: string; role: string } | null;
}

export interface Lane {
  id: string;
  label: string;
  source: "application" | "lead";
  count: number;
  cards: Card[];
}

export interface Summary {
  remaining_to_apply: number;
  awaiting_response: number;
  in_interview: number;
  offers: number;
  closed: number;
  needs_outcome: number;
}

export interface Board {
  lanes: Lane[];
  summary: Summary;
}

export const CSV_STATUSES = [
  "applied", "interview", "offer",
  "hired", "rejected", "no response", "withdrawn", "offer declined",
];

export const SEEN_STATUSES = ["new", "evaluated", "ranked", "skipped", "expired"];

// Lanes that accept a dropped application card. applied/interview/offer map to a
// single status; "closed" maps to several outcomes, so it drops with a sentinel
// that App resolves by prompting for the specific closing status.
export const CLOSED_DROP = "__pick_closed__";
export const DROP_LANES: Record<string, string> = {
  applied: "applied",
  interview: "interview",
  offer: "offer",
  closed: CLOSED_DROP,
};
