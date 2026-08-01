import { useState } from "react";
import type { Card } from "./types";
import { CSV_STATUSES, SEEN_STATUSES } from "./types";

interface Props {
  card: Card;
  onAppStatus: (id: string, status: string) => void;
  onAppNotes: (id: string, notes: string) => void;
  onLeadStatus: (url: string, status: string) => void;
  onDismiss: (id: string) => void;
}

function scoreClass(score?: number | null): string {
  if (score == null) return "";
  if (score >= 75) return "score strong";
  if (score >= 60) return "score good";
  if (score >= 45) return "score moderate";
  return "score weak";
}

export default function CardView({
  card, onAppStatus, onAppNotes, onLeadStatus, onDismiss,
}: Props) {
  const [open, setOpen] = useState(false);
  const [notes, setNotes] = useState(card.notes ?? "");
  const isApp = card.source === "application";

  return (
    <article
      className={`card ${card.won ? "won" : ""}`}
      draggable={isApp}
      onDragStart={(e) => {
        e.dataTransfer.setData("text/card-id", card.id);
        e.dataTransfer.effectAllowed = "move";
      }}
    >
      <header className="card-head" onClick={() => setOpen((o) => !o)}>
        <div className="card-title">
          <strong>{card.company}</strong>
          <span className="role">{card.role}</span>
        </div>
        <div className="badges">
          {card.rank_score != null && (
            <span className={scoreClass(card.rank_score)}>{card.rank_score}</span>
          )}
          {card.rank_verdict && <span className="verdict">{card.rank_verdict}</span>}
          {isApp && card.fit_rating && <span className="verdict">fit {card.fit_rating}</span>}
        </div>
      </header>

      {card.location_flag && <p className="flag warn">⚠ {card.location_flag}</p>}

      {card.possible_duplicate && (
        <p className="flag dup">
          Possible duplicate — already applied to “{card.possible_duplicate.role}” here
        </p>
      )}

      {card.needs_outcome && (
        <p className="flag outcome">
          Changed in app — run <code>/outcome {card.company}</code> to archive + calibrate
          <button className="link" onClick={() => onDismiss(card.id)}>dismiss</button>
        </p>
      )}

      {open && (
        <div className="card-body">
          {card.url && (
            <a className="ext" href={card.url} target="_blank" rel="noreferrer">
              open posting ↗
            </a>
          )}

          {isApp ? (
            <>
              <label className="field">
                status
                <select
                  value={card.status}
                  onChange={(e) => onAppStatus(card.id, e.target.value)}
                >
                  {CSV_STATUSES.map((s) => (
                    <option key={s} value={s}>{s}</option>
                  ))}
                </select>
              </label>
              <label className="field">
                notes
                <textarea
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  rows={3}
                />
              </label>
              {notes !== (card.notes ?? "") && (
                <button className="save" onClick={() => onAppNotes(card.id, notes)}>
                  save notes
                </button>
              )}
              {card.date && <p className="meta">applied {card.date} · {card.channel}</p>}
              {card.cv_file && <p className="meta path">{card.cv_file}</p>}
            </>
          ) : (
            <>
              <label className="field">
                status
                <select
                  value={card.status}
                  onChange={(e) => onLeadStatus(card.url, e.target.value)}
                >
                  {SEEN_STATUSES.map((s) => (
                    <option key={s} value={s}>{s}</option>
                  ))}
                </select>
              </label>
              <p className="hint">
                To apply, run <code>/apply {card.url}</code> in Claude, then <code>/outcome</code> to log it.
                <button
                  className="link"
                  onClick={() => navigator.clipboard.writeText(`/apply ${card.url}`)}
                >
                  copy
                </button>
              </p>
            </>
          )}
        </div>
      )}
    </article>
  );
}
