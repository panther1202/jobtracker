# builtin-search CLI

Zero-dependency Bun CLI for searching jobs on [Built In](https://builtin.com)
(US tech/startup market). Personal use only — see the warning in `../SKILL.md`.

## Install

```bash
cd .agents/skills/builtin-search/cli && bun install && cd ../../../..
```

`bun install` only pulls TypeScript dev types — there are **no runtime
dependencies**. The CLI runs with plain `bun`.

## Usage

```bash
# Search (at least --query or --location required; results are US-only)
bun run src/cli.ts search -q "AI Engineer" --format table
bun run src/cli.ts search -q "Machine Learning Engineer" -l "New York" --jobage 7
bun run src/cli.ts search -q "Python Developer" --remote remote --limit 10

# Detail (pass a result URL)
bun run src/cli.ts detail https://builtin.com/job/sr-ml-ai-engineer/9970751 --format plain
```

Flags: `--query/-q`, `--location/-l`, `--remote <remote|hybrid|onsite>`,
`--jobage <1|7|14|30>`, `--page <n>`, `--limit/-n <n>`, `--format <json|table|plain>`.

## Scripts

- `bun run start` — run the CLI
- `bun run test` — live smoke tests + arg validation (`bun test`)
- `bun run typecheck` — `tsc --noEmit`

## How it works

- **US-only:** always sends `country=USA` (Built In geo-defaults otherwise).
- **Search:** parses server-rendered job cards from `/jobs` (chunked regex, one
  card at a time so a malformed card can't break the rest).
- **Detail:** parses the schema.org `JobPosting` JSON-LD from `/job/<slug>/<id>`.
  Note the two Built In quirks handled in `helpers.ts`: the ld+json script type is
  HTML-encoded (`application/ld&#x2B;json`) and the posting is nested in an
  `@graph` wrapper.

See `../url-reference.md` for the full endpoint/parsing map.
