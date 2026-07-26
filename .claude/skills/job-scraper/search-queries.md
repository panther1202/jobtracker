# Search Queries for Job Scraper

<!-- SETUP: Customize these queries based on your skills, target roles, and location -->

## Search Sites

Panth is based in the USA, not Denmark, so the shipped Danish portal CLIs (Jobindex, Jobbank, Jobdanmark, Jobnet) do not apply here.

Primary (structured CLI sources):
- **linkedin-search CLI** (`.agents/skills/linkedin-search`) - LinkedIn's public job listings, zero runtime dependencies, takes an explicit location flag (e.g. `-l "Somerset, NJ"`, `-l "Remote"`, `-l "United States"`). Personal use only - keep query volume low.
- **builtin-search CLI** (`.agents/skills/builtin-search`) - Built In (builtin.com) US tech/startup job listings, zero runtime dependencies, US-only by default (`country=USA`). Good for AI/startup roles. `-q` keyword, optional `-l` location hint, `--remote remote`. Personal use only.

Secondary (company career pages / general web via Google):
- Direct Google searches with `site:` filters for known target companies or boards (e.g. `site:indeed.com`, `site:lever.co`, `site:greenhouse.io`). Note: Dice was evaluated for a dedicated CLI but its robots.txt disallows the search paths and its API is auth-gated, so it stays a manual `site:` source.

To add another dedicated US job-board CLI, run `/add-portal` and point it at the board - it scaffolds and test-runs a new skill the same way the shipped ones were built.

## Query Categories

Queries are grouped by priority. Combine with location terms where the site supports it - Panth has no commute or relocation constraints, so default to a broad net (remote + nationwide US).

### Priority 1: Software Engineer / AI Engineer (Python)

These match Panth's strongest and most desired career direction.

```
linkedin-search "AI Engineer" -l "United States"
linkedin-search "Software Engineer Python" -l "United States"
builtin-search -q "AI Engineer"
builtin-search -q "Software Engineer Python"
site:indeed.com "AI Engineer" Python remote
site:indeed.com "Software Engineer" Python remote
```

### Priority 2: Applied AI / Healthcare AI

These match Panth's domain expertise - applied LLM/AI engineering, with a growing edge in healthcare-adjacent AI (IONM data processing, insurance-claims automation).

```
linkedin-search "Machine Learning Engineer" -l "United States"
linkedin-search "AI Engineer healthcare" -l "United States"
builtin-search -q "Machine Learning Engineer"
builtin-search -q "LLM Engineer"
site:indeed.com "LangChain" OR "LLM engineer" remote
site:indeed.com "AI Engineer" healthcare Python
```

### Priority 3: Backend Engineer / Full Stack Engineer

Adjacent roles Panth could pivot into.

```
linkedin-search "Backend Engineer" Python -l "United States"
linkedin-search "Full Stack Engineer" Python -l "United States"
site:indeed.com "Backend Engineer" Python remote
site:indeed.com "Full Stack Engineer" Python remote
```

### Priority 4: Broader Technical / Python Developer

Wider net for general technical roles.

```
linkedin-search "Python Developer" -l "United States"
site:indeed.com "Python Developer" remote
site:indeed.com "Software Developer" Python AWS
```

## Location Filter

Panth has no commute or relocation constraints. Treat all US locations (remote or on-site) as acceptable by default:
- Somerset, NJ and surrounding NJ/NYC metro area (ideal - home base)
- Remote (US) - acceptable
- Anywhere else in the United States - acceptable (open to relocation)
- International roles requiring relocation - flag for confirmation before proceeding (not yet discussed with Panth)

## Date Filter

Only include jobs posted within the last 14 days, or with an application deadline that has not yet passed. If a posting date cannot be determined, include it but flag as "date unknown".

## Adapting Queries

If the user specifies a focus area, select queries from the matching category and also generate 2-3 custom queries for that focus. For example:
- "/scrape [focus_area]" -> relevant category queries + custom focus-specific queries
