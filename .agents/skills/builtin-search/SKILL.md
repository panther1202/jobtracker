---
name: builtin-search
version: 1.0.0
description: >
  Use this skill to search for jobs on Built In (builtin.com), a US tech and
  startup job board, or to look up a specific Built In posting. Covers AI/ML,
  software engineering, data, product, and design roles at US startups and tech
  companies, including remote roles. US market, English-language postings.
  Trigger phrases: find a job, job search, search for jobs, tech jobs, startup
  jobs, AI jobs, remote tech jobs, "any X jobs on Built In", "search builtin",
  look up this Built In posting.
context: fork
allowed-tools: Bash(bun run skills/builtin-search/cli/src/cli.ts *)
---

# Built In Search Skill

Search live job listings from Built In (builtin.com), a **US** tech/startup job
board. No authentication, no API key, and **zero runtime dependencies** — it runs
with just `bun`. Results are restricted to the US market (`country=USA`).

## ⚠️ Personal use only

This reads Built In's public job pages. Built In's `robots.txt` permits `/jobs`
and `/job/` (only `/search/`, `/user/`, `/admin/` and similar are disallowed), so
this stays within their crawl rules — but **keep volume low and do not use it
commercially or for bulk data collection.** Run it on your own responsibility.

## When to use this skill

- Search US tech/startup job openings by keyword (and optionally remote)
- Filter by recency (posted within 1 / 7 / 14 / 30 days)
- Get the full description of a specific Built In posting

## Commands

### Search job listings

```bash
bun run skills/builtin-search/cli/src/cli.ts search [flags]
```

Key flags:
- `--query` / `-q <text>` — keyword search (title, skill, role). Recommended.
- `--location` / `-l <text>` — a city/region hint; it is folded into the keyword
  search (Built In has no reliable standalone city parameter on the public page).
  The country is always USA regardless. Use `-l "Remote"` to bias toward remote.
- `--remote <mode>` — `remote` maps to Built In's remote filter; `hybrid`/`onsite`
  are accepted but only `remote` changes the query (workplace type is reported
  per result in the output instead).
- `--jobage <days>` — posted within N days; snaps to Built In's buckets (1/7/14/30).
- `--page <n>` — 1-indexed page.
- `--limit` / `-n <n>` — cap total results emitted (client-side).
- `--format json|table|plain` — default `json`.

At least one of `--query` or `--location` is required.

### Fetch full job detail

```bash
bun run skills/builtin-search/cli/src/cli.ts detail <id|url> [--format json|plain]
```

Pass a Built In job URL (`https://builtin.com/job/<slug>/<id>`) from `search`
results, or a full URL. Returns the full description, company, location,
employment type, posting date, and apply URL (parsed from the posting's
schema.org JobPosting JSON-LD). A URL is preferred over a bare id because Built
In detail pages are addressed as `/job/<slug>/<id>`.

## Usage examples

```bash
# AI Engineer roles, US, quick scan
bun run skills/builtin-search/cli/src/cli.ts search -q "AI Engineer" --format table

# ML Engineer near New York, last 7 days
bun run skills/builtin-search/cli/src/cli.ts search -q "Machine Learning Engineer" -l "New York" --jobage 7 --format table

# Remote Python roles
bun run skills/builtin-search/cli/src/cli.ts search -q "Python Developer" --remote remote --format table

# Cap to 10 LLM roles
bun run skills/builtin-search/cli/src/cli.ts search -q "LLM Engineer" --limit 10

# Full detail for a specific posting
bun run skills/builtin-search/cli/src/cli.ts detail https://builtin.com/job/sr-ml-ai-engineer/9970751 --format plain
```

## Output formats

| Format | Best for |
|--------|----------|
| `json` | Default — programmatic use, passing a result URL to `detail` |
| `table` | Quick human-readable scanning |
| `plain` | Reading a single job's full detail (`detail` command) |

JSON search shape: `{ "meta": { "count", "page" }, "results": [ { id, title, company, companyUrl, location, workplaceType, date, url } ] }`. Missing values are `null`.

All errors are written to **stderr** as `{ "error": "...", "code": "..." }` and the process exits with code `1`.

## Notes

- **US-only by design.** The CLI always sends `country=USA`; without it, Built In
  geo-defaults to the caller's region (e.g. India from a non-US IP).
- **Dates are relative text** as Built In renders them ("Posted 3 Days Ago",
  "Reposted 21 Hours Ago", "Yesterday") in search results; the `detail` command
  returns an absolute ISO `datePosted` from the posting's JSON-LD.
- **Workplace type** (Remote / Hybrid / In-Office) is reported per result from the
  card, separate from the location.
- Built In may rate-limit; the CLI retries 429/5xx with exponential backoff. Keep
  volume low (see the personal-use note above).
- If Built In changes its markup, `url-reference.md` records the parsing anchors.
