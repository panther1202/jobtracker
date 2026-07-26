# Built In (builtin.com) - endpoint & parsing reference

Reconnaissance notes for maintaining `builtin-search` when the portal changes.
Data source: Built In's public, unauthenticated job pages. Verified 2026-07-24.

## Access

- `robots.txt`: `/jobs` and `/job/` are **allowed**. Disallowed paths that do NOT
  affect this skill: `/search/`, `/user/`, `/admin/`, `/profiles/`, `/companies/*`
  facet pages, `/dashboard/`, `/member(s)/`. No auth wall on search or detail.
- No API key. Server-rendered HTML (no JS execution needed).

## Search

- **URL:** `https://builtin.com/jobs`
- **Parameters:**

| Param | Purpose | Notes |
|-------|---------|-------|
| `country` | market filter | **Always `USA`** in this skill. Omitting it makes Built In geo-default to the caller's region (India from a non-US IP). This is the single most important param. |
| `search` | keyword box | Title/skill/role. A `--location` city hint is folded in here (no reliable standalone city param). |
| `daysSinceUpdated` | posting age | Discrete buckets: `1`, `7`, `14`, `30`. |
| `remote` | remote filter | `true` for remote-only. |
| `page` | pagination | 1-indexed; omit for page 1. |

- **Search result card structure** (one per posting):
  - Container: `<div id="job-card-<ID>" data-id="job-card" x-init="initObserver(<ID>, ...)">`. The skill splits the HTML on `<div id="job-card-(\d+)"` to get the id and per-card chunk.
  - Title + job URL: `<a href="/job/<slug>/<ID>" ... data-id="job-card-title" ...>TITLE</a>`
  - Company: `<a href="/company/<slug>" ... data-id="company-title" ...><span>NAME</span></a>`
  - Location: `<span>` following an `<i class="... fa-location-dot ...">` icon.
  - Workplace type: `<span>` following an `<i class="... fa-house-building ...">` icon (Remote / Hybrid / In-Office).
  - Date (relative): text between `</i>` and `</span>` following an `<i class="... fa-clock ...">` icon (e.g. "Posted 3 Days Ago", "Reposted 21 Hours Ago", "Yesterday"). The icon carries a long class list, so the parser allows up to ~240 chars between `fa-clock` and `</i>`.
  - There is also a JSON-LD `ItemList` (schema.org) with `name`/`url`/`description` per posting, and a small `id="jobsListServerData"` blob that holds only skill facets (not the jobs) — the HTML cards are the authoritative source for company/location/date.

## Detail

- **URL:** `https://builtin.com/job/<slug>/<ID>` (slug recoverable from a search result URL; a bare id falls back to `/job/j/<ID>`, which Built In redirects).
- **Primary parse source:** a schema.org `JobPosting` embedded as JSON-LD.
  - **Gotcha:** the script tag's type is HTML-entity-encoded — `type="application/ld&#x2B;json"` (the `+` is `&#x2B;`), so a naive `application/ld\+json` match fails. The parser matches `type="[^"]*ld[^"]*json"` instead.
  - **Gotcha:** the JobPosting sits inside an `@graph` array wrapper, so the parser descends recursively (`findJobPosting`) rather than checking only the top-level `@type`.
  - Fields used: `title`, `hiringOrganization.name`, `jobLocation[].address.{addressLocality,addressRegion,addressCountry}`, `description` (HTML — tags stripped, `<br>`/block-close turned into newlines), `employmentType`, `datePosted`, `url` (apply link).
  - Fallback title: the page `<h1>` if JSON-LD is absent.

## Output contract (shared across all portal skills)

- JSON: `{ "meta": { "count", "page" }, "results": [ { id, title, company, companyUrl, location, workplaceType, date, url } ] }`; missing values `null`.
- Errors: stderr `{ "error", "code" }`, exit `1`.
- Fetch: browser UA, exponential backoff + jitter on 429/5xx (max 6 retries), `""` on 404.
