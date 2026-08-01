import { useEffect, useMemo, useState } from "react";
import * as api from "./api";
import Lane from "./Lane";
import type { Board } from "./types";
import { CLOSED_DROP } from "./types";

export default function App() {
  const [board, setBoard] = useState<Board | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [query, setQuery] = useState("");
  const [showArchived, setShowArchived] = useState(false);

  const load = () =>
    api.getBoard().then(setBoard).catch((e) => setError(String(e.message ?? e)));

  useEffect(() => {
    load();
  }, []);

  // Any mutation returns the fresh board, so handlers just swap state in.
  const run = (p: Promise<Board>) =>
    p.then(setBoard).catch((e) => setError(String(e.message ?? e)));

  const handlers = {
    onAppStatus: (id: string, status: string) => {
      let s = status;
      if (s === CLOSED_DROP) {
        const choice = window.prompt(
          "Close as which status?\nhired / rejected / no response / withdrawn / offer declined",
          "rejected",
        );
        if (!choice) return;
        s = choice.trim().toLowerCase();
      }
      return run(api.patchApplication(id, { status: s }));
    },
    onAppNotes: (id: string, notes: string) =>
      run(api.patchApplication(id, { notes })),
    onLeadStatus: (url: string, status: string) => run(api.patchLead(url, status)),
    onDismiss: (id: string) => run(api.dismissPending(id)),
  };

  const lanes = useMemo(() => {
    if (!board) return [];
    const q = query.trim().toLowerCase();
    return board.lanes
      .filter((l) => showArchived || l.id !== "archived")
      .map((l) => ({
        ...l,
        cards: q
          ? l.cards.filter(
              (c) =>
                c.company.toLowerCase().includes(q) ||
                c.role.toLowerCase().includes(q),
            )
          : l.cards,
      }));
  }, [board, query, showArchived]);

  if (error) {
    return (
      <div className="error-screen">
        <h1>Can’t reach the tracker API</h1>
        <p>{error}</p>
        <p className="muted">
          Start the backend: <code>uvicorn app:app --port 8100</code> from{" "}
          <code>tracker/backend/</code>.
        </p>
        <button onClick={() => { setError(null); load(); }}>retry</button>
      </div>
    );
  }

  if (!board) return <div className="loading">Loading board…</div>;

  const s = board.summary;
  return (
    <div className="app">
      <header className="topbar">
        <h1>Job Tracker</h1>
        <div className="chips">
          <span className="chip accent">{s.remaining_to_apply} to apply</span>
          <span className="chip">{s.awaiting_response} awaiting</span>
          <span className="chip">{s.in_interview} interview</span>
          <span className="chip">{s.offers} offer</span>
          <span className="chip">{s.closed} closed</span>
          {s.needs_outcome > 0 && (
            <span className="chip warn">{s.needs_outcome} need /outcome</span>
          )}
        </div>
        <div className="controls">
          <input
            placeholder="filter company / role…"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <label className="toggle">
            <input
              type="checkbox"
              checked={showArchived}
              onChange={(e) => setShowArchived(e.target.checked)}
            />
            archived
          </label>
          <button onClick={load}>refresh</button>
        </div>
      </header>

      <main className="board">
        {lanes.map((lane) => (
          <Lane key={lane.id} lane={lane} {...handlers} />
        ))}
      </main>
    </div>
  );
}
