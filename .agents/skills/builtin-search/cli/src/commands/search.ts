import {
  BASE,
  SEARCH_PATH,
  htmlFetch,
  parseJobCards,
  jobageParam,
  writeError,
  type JobCard,
} from "../helpers.js"

export interface SearchOpts {
  query?: string
  location?: string
  jobage: number
  remote?: string // "remote" | "hybrid" | "onsite"
  page: number
  limit?: number
  format: "json" | "table" | "plain"
}

function buildUrl(opts: SearchOpts): string {
  const params = new URLSearchParams()
  // US-market skill: country=USA restricts results to US postings (without it,
  // Built In geo-defaults to the caller's region, e.g. India from a non-US IP).
  params.set("country", "USA")
  // Built In treats the keyword box as `search`. A city-level location is not a
  // reliable standalone query param, so a provided --location is folded into the
  // keyword string (documented in SKILL.md); country stays USA regardless.
  const keywords = [opts.query, opts.location].filter(Boolean).join(" ")
  if (keywords) params.set("search", keywords)
  const age = jobageParam(opts.jobage)
  if (age) params.set("daysSinceUpdated", age)
  if (opts.remote && opts.remote.toLowerCase() === "remote") params.set("remote", "true")
  if (opts.page > 1) params.set("page", String(opts.page))
  return `${BASE}${SEARCH_PATH}?${params.toString()}`
}

function renderTable(cards: JobCard[]): string {
  if (cards.length === 0) return "No results."
  const rows = cards.map((c) => {
    const title = (c.title || "").slice(0, 40).padEnd(40)
    const company = (c.company || "—").slice(0, 24).padEnd(24)
    const loc = (c.location || "—").slice(0, 22).padEnd(22)
    const wt = (c.workplaceType || "—").slice(0, 8).padEnd(8)
    const date = c.date || "—"
    return `${c.id.padEnd(10)} ${title} ${company} ${loc} ${wt} ${date}`
  })
  const header =
    "ID".padEnd(10) +
    " " +
    "TITLE".padEnd(40) +
    " " +
    "COMPANY".padEnd(24) +
    " " +
    "LOCATION".padEnd(22) +
    " " +
    "TYPE".padEnd(8) +
    " DATE"
  return [header, "-".repeat(header.length), ...rows].join("\n")
}

export async function runSearch(opts: SearchOpts): Promise<number> {
  try {
    const html = await htmlFetch(buildUrl(opts))
    let cards = parseJobCards(html)
    if (opts.limit && opts.limit > 0) cards = cards.slice(0, opts.limit)

    if (opts.format === "table") {
      process.stdout.write(renderTable(cards) + "\n")
    } else if (opts.format === "plain") {
      process.stdout.write(
        cards
          .map(
            (c) =>
              `${c.title}\n  ${c.company || "—"} · ${c.location || "—"} · ${c.workplaceType || "—"} · ${c.date || "—"}\n  id: ${c.id}\n  ${c.url}`,
          )
          .join("\n\n") + "\n",
      )
    } else {
      process.stdout.write(
        JSON.stringify(
          { meta: { count: cards.length, page: opts.page }, results: cards },
          null,
          2,
        ) + "\n",
      )
    }
    return 0
  } catch (e) {
    writeError(e instanceof Error ? e.message : String(e), "SEARCH_FAILED")
    return 1
  }
}
