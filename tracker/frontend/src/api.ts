import type { Board } from "./types";

async function json<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let detail = res.statusText;
    try {
      detail = (await res.json()).detail ?? detail;
    } catch {
      /* non-JSON error body */
    }
    throw new Error(`${res.status}: ${detail}`);
  }
  return res.json() as Promise<T>;
}

export function getBoard(): Promise<Board> {
  return fetch("/api/board").then((r) => json<Board>(r));
}

export function patchApplication(
  id: string,
  body: { status?: string; notes?: string },
): Promise<Board> {
  return fetch("/api/application", {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id, ...body }),
  }).then((r) => json<Board>(r));
}

export function patchLead(url: string, status: string): Promise<Board> {
  return fetch("/api/lead", {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url, status }),
  }).then((r) => json<Board>(r));
}

export function dismissPending(id: string): Promise<Board> {
  return fetch("/api/pending/dismiss", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id }),
  }).then((r) => json<Board>(r));
}
