import { BASE, htmlFetch, parseJobDetail, writeError } from "../helpers.js"

export interface DetailOpts {
  id: string
  format: "json" | "plain"
}

/**
 * Accept a Built In job URL (/job/<slug>/<id>), a bare numeric id, or a full URL.
 * Returns { id, url } — the URL is needed because Built In detail pages live at
 * /job/<slug>/<id>, and the slug is recoverable from a passed URL but not from a
 * bare id. For a bare id we fall back to the id-only path, which Built In redirects.
 */
function normalize(input: string): { id: string; url: string } | null {
  const m = input.match(/\/job\/([a-z0-9-]+)\/(\d+)/i)
  if (m) return { id: m[2], url: `${BASE}/job/${m[1]}/${m[2]}` }
  const bare = input.match(/^(\d{4,})$/)
  if (bare) return { id: bare[1], url: `${BASE}/job/j/${bare[1]}` }
  const anyId = input.match(/(\d{4,})/)
  if (anyId) return { id: anyId[1], url: `${BASE}/job/j/${anyId[1]}` }
  return null
}

export async function runDetail(opts: DetailOpts): Promise<number> {
  const norm = normalize(opts.id)
  if (!norm) {
    writeError(`Could not parse a job id/url from "${opts.id}"`, "BAD_ID")
    return 1
  }
  try {
    const html = await htmlFetch(norm.url)
    if (!html) {
      writeError("Job not found", "NOT_FOUND")
      return 1
    }
    const job = parseJobDetail(html, norm.id, norm.url)

    if (opts.format === "plain") {
      const lines = [
        job.title,
        `${job.company || "—"} · ${job.location || "—"}`,
        "",
        job.employmentType ? `Employment: ${job.employmentType}` : "",
        job.datePosted ? `Posted: ${job.datePosted}` : "",
        "",
        job.description || "(no description)",
        "",
        `URL: ${job.url}`,
        job.applyUrl ? `Apply: ${job.applyUrl}` : "",
      ].filter((l) => l !== "")
      process.stdout.write(lines.join("\n") + "\n")
    } else {
      process.stdout.write(JSON.stringify(job, null, 2) + "\n")
    }
    return 0
  } catch (e) {
    writeError(e instanceof Error ? e.message : String(e), "DETAIL_FAILED")
    return 1
  }
}
