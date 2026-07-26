import { useState } from "react";
import CardView from "./CardView";
import type { Card, Lane as LaneModel } from "./types";
import { DROP_LANES } from "./types";

interface Props {
  lane: LaneModel;
  onAppStatus: (id: string, status: string) => void;
  onAppNotes: (id: string, notes: string) => void;
  onLeadStatus: (url: string, status: string) => void;
  onDismiss: (id: string) => void;
}

export default function Lane({ lane, ...handlers }: Props) {
  const [dragOver, setDragOver] = useState(false);
  const dropStatus = DROP_LANES[lane.id];

  return (
    <section
      className={`lane ${dragOver ? "drag-over" : ""} ${dropStatus ? "droppable" : ""}`}
      onDragOver={(e) => {
        if (dropStatus) {
          e.preventDefault();
          setDragOver(true);
        }
      }}
      onDragLeave={() => setDragOver(false)}
      onDrop={(e) => {
        setDragOver(false);
        if (!dropStatus) return;
        const id = e.dataTransfer.getData("text/card-id");
        if (id) handlers.onAppStatus(id, dropStatus);
      }}
    >
      <header className="lane-head">
        <span>{lane.label}</span>
        <span className="count">{lane.count}</span>
      </header>
      <div className="lane-cards">
        {lane.cards.map((card: Card) => (
          <CardView key={card.id} card={card} {...handlers} />
        ))}
        {lane.cards.length === 0 && <p className="empty">—</p>}
      </div>
    </section>
  );
}
