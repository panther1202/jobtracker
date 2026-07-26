// Data source: Built In (builtin.com) public job pages. No authentication required.
// The search page (/jobs?search=...) is server-rendered HTML with a flat list of
// job cards; the detail page (/job/<slug>/<id>) carries a schema.org JobPosting
// JSON-LD block. We parse both with regex + JSON.parse of the embedded JSON-LD;
// each card is parsed independently so one malformed card cannot break the rest.

export const BASE = "https://builtin.com"
export const SEARCH_PATH = "/jobs"

export function writeError(error: string, code: string): void {
  process.stderr.write(JSON.stringify({ error, code }) + "\n")
}

const UA =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " +
  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

/** Fetch HTML with exponential backoff on 429/5xx. Returns "" on a 404. */
export async function htmlFetch(url: string): Promise<string> {
  const maxRetries = 6
  let delay = 500
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    const response = await fetch(url, {
      headers: {
        "User-Agent": UA,
        Accept: "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
      },
      redirect: "follow",
    })
    if (response.status === 429 || response.status >= 500) {
      if (attempt === maxRetries) {
        throw new Error(`Request failed: ${response.status} ${response.statusText}`)
      }
      const jitter = Math.floor(Math.random() * 500)
      await new Promise((r) => setTimeout(r, delay + jitter))
      delay = Math.min(delay * 2, 8000)
      continue
    }
    if (response.status === 404) return ""
    if (!response.ok) {
      throw new Error(`Request failed: ${response.status} ${response.statusText}`)
    }
    return response.text()
  }
  throw new Error("Request failed after max retries")
}

export interface JobCard {
  id: string
  title: string
  company: string | null
  companyUrl: string | null
  location: string | null
  workplaceType: string | null
  date: string | null
  url: string
}

export interface JobDetail extends JobCard {
  description: string | null
  employmentType: string | null
  datePosted: string | null
  applyUrl: string | null
}

function numericEntity(cp: number): string {
  return cp >= 0 && cp <= 0x10ffff ? String.fromCodePoint(cp) : ""
}

function decodeHtmlEntities(text: string): string {
  return text
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&apos;/g, "'")
    .replace(/&#(\d+);/g, (_, dec) => numericEntity(parseInt(dec, 10)))
    .replace(/&#[xX]([0-9a-fA-F]+);/g, (_, hex) => numericEntity(parseInt(hex, 16)))
    .replace(/&nbsp;/g, " ")
}

function stripTags(html: string): string {
  return html.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim()
}

function clean(html: string): string {
  return decodeHtmlEntities(stripTags(html))
}

/**
 * Parse the search results page. Built In renders each posting as a
 * `<div id="job-card-<ID>" ...>` block. We split on that marker and parse each
 * chunk independently. Fields are anchored on stable `data-id` attributes and
 * FontAwesome icon classes (see url-reference.md).
 */
export function parseJobCards(html: string): JobCard[] {
  const results: JobCard[] = []
  const chunks = html.split(/<div\s+id="job-card-(\d+)"/i).slice(1)

  // After split, chunks alternate: [id, body, id, body, ...]
  for (let i = 0; i + 1 < chunks.length; i += 2) {
    const id = chunks[i]
    const chunk = chunks[i + 1]

    // Title + job URL: <a href="/job/<slug>/<id>" data-id="job-card-title" ...>TITLE</a>
    const titleMatch = chunk.match(
      /href="(\/job\/[^"]+)"[^>]*data-id="job-card-title"[^>]*>([\s\S]*?)<\/a>/i,
    )
    if (!titleMatch) continue
    const url = BASE + decodeHtmlEntities(titleMatch[1]).split("?")[0]
    const title = clean(titleMatch[2])
    if (!title) continue

    // Company: <a href="/company/<slug>" data-id="company-title" ...><span>NAME</span></a>
    let company: string | null = null
    let companyUrl: string | null = null
    const companyMatch = chunk.match(
      /href="(\/company\/[^"]+)"[^>]*data-id="company-title"[^>]*>([\s\S]*?)<\/a>/i,
    )
    if (companyMatch) {
      companyUrl = BASE + decodeHtmlEntities(companyMatch[1]).split("?")[0]
      company = clean(companyMatch[2]) || null
    }

    // Location: span following the fa-location-dot icon.
    let location: string | null = null
    const locMatch = chunk.match(
      /fa-location-dot[\s\S]{0,180}?<span[^>]*>([\s\S]*?)<\/span>/i,
    )
    if (locMatch) location = clean(locMatch[1]) || null

    // Workplace type: span following the fa-house-building icon (Remote/Hybrid/On-site).
    let workplaceType: string | null = null
    const wtMatch = chunk.match(
      /fa-house-building[\s\S]{0,180}?<span[^>]*>([\s\S]*?)<\/span>/i,
    )
    if (wtMatch) workplaceType = clean(wtMatch[1]) || null

    // Date: text following the fa-clock icon, e.g. "Posted 3 Days Ago" / "Reposted 21 Hours Ago".
    let date: string | null = null
    const dateMatch = chunk.match(/fa-clock[\s\S]{0,240}?<\/i>([\s\S]*?)<\/span>/i)
    if (dateMatch) date = clean(dateMatch[1]) || null

    results.push({ id, title, company, companyUrl, location, workplaceType, date, url })
  }

  return results
}

/** Recursively locate a schema.org JobPosting node (handles @graph and arrays). */
function findJobPosting(node: unknown): Record<string, unknown> | null {
  if (Array.isArray(node)) {
    for (const item of node) {
      const found = findJobPosting(item)
      if (found) return found
    }
    return null
  }
  if (node && typeof node === "object") {
    const obj = node as Record<string, unknown>
    if (obj["@type"] === "JobPosting") return obj
    for (const v of Object.values(obj)) {
      const found = findJobPosting(v)
      if (found) return found
    }
  }
  return null
}

/**
 * Pull the first schema.org JobPosting object from a page's JSON-LD blocks.
 * The script type is HTML-encoded on Built In (`application/ld&#x2B;json`), and
 * the posting sits inside an `@graph` wrapper — hence the loose type match and
 * the recursive descent.
 */
function extractJobPostingLd(html: string): Record<string, unknown> | null {
  const re = /<script[^>]*type="[^"]*ld[^"]*json"[^>]*>([\s\S]*?)<\/script>/gi
  let m: RegExpExecArray | null
  while ((m = re.exec(html)) !== null) {
    let data: unknown
    try {
      data = JSON.parse(m[1].trim())
    } catch {
      continue
    }
    const found = findJobPosting(data)
    if (found) return found
  }
  return null
}

function asString(v: unknown): string | null {
  return typeof v === "string" && v.trim() ? v.trim() : null
}

/** Parse a single job detail page, preferring the schema.org JobPosting JSON-LD. */
export function parseJobDetail(html: string, id: string, url: string): JobDetail {
  const ld = extractJobPostingLd(html)

  let title: string | null = null
  let company: string | null = null
  let location: string | null = null
  let description: string | null = null
  let employmentType: string | null = null
  let datePosted: string | null = null
  let applyUrl: string | null = null

  if (ld) {
    title = asString(ld["title"])
    const org = ld["hiringOrganization"]
    if (org && typeof org === "object") company = asString((org as Record<string, unknown>)["name"])
    const loc = ld["jobLocation"]
    if (loc) {
      const first = Array.isArray(loc) ? loc[0] : loc
      const addr = first && typeof first === "object" ? (first as Record<string, unknown>)["address"] : null
      if (addr && typeof addr === "object") {
        const a = addr as Record<string, unknown>
        location = [asString(a["addressLocality"]), asString(a["addressRegion"]), asString(a["addressCountry"])]
          .filter(Boolean)
          .join(", ") || null
      }
    }
    const rawDesc = asString(ld["description"])
    if (rawDesc) {
      description =
        decodeHtmlEntities(
          stripTags(rawDesc.replace(/<\s*br\s*\/?>/gi, "\n").replace(/<\/(p|li|ul|ol|div|h\d)>/gi, "\n")),
        ).replace(/\n{3,}/g, "\n\n").trim() || null
    }
    employmentType = asString(ld["employmentType"])
    datePosted = asString(ld["datePosted"])
    const apply = ld["url"]
    applyUrl = asString(apply)
  }

  // Fallback title from the <h1> if JSON-LD was absent.
  if (!title) {
    const h1 = html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i)
    title = h1 ? clean(h1[1]) : "(untitled)"
  }

  return {
    id,
    title,
    company,
    companyUrl: null,
    location,
    workplaceType: null,
    date: datePosted,
    url,
    description,
    employmentType,
    datePosted,
    applyUrl,
  }
}

/** Map a job-age in days to Built In's daysSinceUpdated parameter (1/7/14/30). */
export function jobageParam(days: number): string | null {
  if (!days || days <= 0 || days >= 9999) return null
  // Built In supports discrete buckets; snap to the nearest supported value.
  const buckets = [1, 7, 14, 30]
  const snapped = buckets.find((b) => days <= b) ?? 30
  return String(snapped)
}
