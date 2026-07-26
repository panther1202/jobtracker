# CV Templates and Tailoring Guide

<!-- SETUP: Profile statements and section ordering are personalized by running /setup -->

## Template: HTML rendered to PDF

All CVs are written as a single self-contained HTML file and rendered to PDF with `tools/render_pdf.py` (xhtml2pdf / the `pisa` library, pure Python, no TeX to install). The layout is single-column with a real text layer, which is ATS-friendly.

**Output file:** `cv/main_<company>.html` (the renderer writes `cv/main_<company>.pdf` alongside it)
**Render with:** `python tools/render_pdf.py`
**Master reference:** `cv/main_example.html` (the tracked template with `[PLACEHOLDER]` tokens; `/setup` fills the tokens and `/apply` copies this structure into `cv/main_<company>.html` and tailors it per role)

### Render command

```bash
python tools/render_pdf.py cv/main_<company>.html
```

The script prints `OK  <path>` on success and `FAILED  <path>` on error. It does **not** report a page count, so you must open the rendered PDF with the Read tool and count the pages yourself. Any page count other than 2 is a failure that must be fixed before presenting to the user.

### Renderer capabilities and limits

xhtml2pdf supports a practical subset of HTML/CSS. Stay inside it:

- **Supported:** `@page { size: letter; margin: ... }`, standard block/inline CSS, `<table>`, `<ul>/<li>`, colors, borders, `font-size` in `pt`, `line-height`, `text-align`, `margin`/`padding`.
- **Not supported:** flexbox, CSS grid, and most advanced/modern CSS. The two-column "role on the left, location/dates on the right" layout is done with a `<table>`, not flexbox.

Do not invent CSS the renderer cannot do. Ground every change in the patterns already present in `cv/main_example.html`.

## Document Structure

The CV is one HTML file. The `<style>` block in the head defines the whole look; the `<body>` holds the content in section order. This is the skeleton (see `cv/main_example.html` for the full template):

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@page { size: letter; margin: 1.5cm 1.6cm; }
body { font-family: Helvetica, Arial, sans-serif; font-size: 10pt; color: #222; line-height: 1.34; }
h1 { color: #2b6cb0; font-size: 24pt; margin: 0 0 2pt 0; letter-spacing: 0.5pt; }
.contact { font-size: 9.5pt; color: #444; margin-bottom: 10pt; }
.contact a { color: #2b6cb0; text-decoration: none; }
.summary { margin: 0 0 12pt 0; text-align: justify; }
h2 { color: #2b6cb0; font-size: 12pt; border-bottom: 1.2pt solid #2b6cb0; padding-bottom: 2pt; margin: 12pt 0 6pt 0; }
.entry { margin-bottom: 8pt; }
.entryhead { width: 100%; }
.entryhead td { vertical-align: top; padding: 0; }
.role { font-weight: bold; font-size: 10.5pt; }
.org { font-style: italic; color: #333; }
.right { text-align: right; color: #555; white-space: nowrap; font-size: 9.5pt; }
ul { margin: 3pt 0 0 0; padding-left: 15pt; }
li { margin-bottom: 2pt; }
.comp li { margin-bottom: 3pt; }
.label { font-weight: bold; }
p { margin: 0; }
</style>
</head>
<body>

<h1>[YOUR_NAME]</h1>
<div class="contact">[YOUR_LOCATION] &nbsp;&bull;&nbsp; <a href="mailto:[YOUR_EMAIL]">[YOUR_EMAIL]</a> &nbsp;&bull;&nbsp; <a href="[YOUR_LINKEDIN_URL]">[YOUR_LINKEDIN_HANDLE]</a></div>

<p class="summary">[PROFILE_STATEMENT - tailored per role]</p>

<h2>Core Competencies</h2>
<ul class="comp"> ... </ul>

<h2>Professional Experience</h2>
<!-- one .entry block per role -->

<h2>Education</h2>
<h2>Certifications</h2>
<h2>Languages</h2>
<h2>References</h2>

</body>
</html>
```

### The style conventions (what each class does)

- **`h1`** is the candidate name, blue (`#2b6cb0`) at 24pt.
- **`.contact`** is a single line under the name: location, email (as a `mailto:` link), and LinkedIn (as text, e.g. `linkedin.com/in/handle`), separated by `&bull;`.
- **`.summary`** is the justified profile statement paragraph. This is the most important section to tailor per role.
- **`h2`** is a blue section header with a blue bottom border.
- **Each role** is a `<div class="entry">` containing a `<table class="entryhead">` (role + organization on the left, location and dates on the right via `class="right"`) followed by a `<ul>` of bullets.
- **`.comp li`** are the Core Competencies bullets; each leads with a bold `<span class="label">` inline label.

Standard section order (as in the master template): summary, Core Competencies, Professional Experience, Education, Certifications, Languages, References. Optional sections such as Independent Projects can be inserted where relevant (see `cv/main_notion.html`).

## Section-by-Section Tailoring

### Profile Statement / Elevator Pitch (Best Practice)
This is the most important section to customize. It is the `<p class="summary">` right after the contact line.

Write 3-4 lines that function as an "elevator pitch": a concise, compelling introduction explaining why you are qualified for *this specific role*. Focus on what the employer gains from hiring you: what you build, the tools you use, and one measurable result.

**Create 2-3 profile statement templates for your main role types:**

<!-- SETUP: These are populated based on your background -->
**For AI Engineer roles:**
> Python developer building applied AI systems, from prompt-engineered LLM pipelines (LangChain, LangGraph, Amazon Bedrock) to production integrations that make existing products AI-compliant. Currently developing an end-to-end AI tool that converts large IONM machine JSON output into CMS 1500 insurance-claim data, cutting manual entry from a full day to under 5 minutes at 85%+ accuracy. Comfortable working independently from problem definition through deployment.

**For Software Engineer / Backend / Full Stack roles:**
> Python developer with production experience across the AI, backend, and QA sides of the software lifecycle. Builds and integrates client-facing tools using Python, SQL, AWS, and Docker, backed by a project-management background (CAPM) that keeps delivery organized. Adaptable across domains, with a growing edge in healthcare-data applications.

### Core Competencies / Skills Section (Best Practice)
Reorder and emphasize based on the role. Use bold category labels (`<span class="label">`).

List **5-7 key competencies** as `<li>` items, tailored to the specific job. For each competency, briefly explain how it adds value to the position.

### Education
- Always include your highest degrees
- For senior roles, keep education brief (dates and titles only)
- Include thesis topics when relevant to the target role

### Professional Experience
- Rewrite bullet points to emphasize aspects most relevant to the target role
- Use 4-5 bullets for most recent role, 2-3 for previous, 1-2 for older
- **Emphasize measurable results** where possible: "Reduced processing time by X%", "Model adopted by the team"

### Handling Employment Gaps (Best Practice)
If there is a gap in your employment history:
- The gap should be explained matter-of-factly if needed
- Describe how professional development continued during the gap
- Frame as deliberate skill-building and career repositioning

### Publications
- Include Google Scholar link if applicable
- Select 3-4 most relevant publications (not always all of them)
- For non-academic roles, keep brief

### Honors and Awards
- Keep format brief, one line each

### References
- List 2-4 references with name, title, company, and contact, or use "Available upon request."
- **Do not attach reference letters** - employers typically contact references directly

## Compile-and-Inspect Loop (MANDATORY)

After writing the CV and before presenting to the user, always render and visually inspect the PDF. Iterate until the layout is clean. Workflow:

1. Run `python tools/render_pdf.py cv/main_<company>.html`
2. Confirm the script printed `OK`
3. Read the rendered `cv/main_<company>.pdf` via the Read tool and count pages: must be exactly 2
4. Visually inspect both pages, checking for awkward page breaks (see below)

### Fixing common page-break problems

Page count is controlled by **content volume** and **CSS** (the `@page` margins, `font-size`, `line-height`, and the `margin`/`padding` on entries in the `<style>` block). xhtml2pdf breaks pages automatically.

**Problem: an entry's heading is split from its bullets across a page break**
Each role's `<div class="entry">` normally stays together as one block. If a break lands awkwardly inside one, add `page-break-inside: avoid;` to the `.entry` rule in the `<style>` block. This is the HTML equivalent of the old `\needspace`:
```html
.entry { margin-bottom: 8pt; page-break-inside: avoid; }
```

**Problem: 3 pages, with real content spilling onto page 3**
Cut content by relevance - do not shrink the font or margins to force-fit. See "Relevance-weighted cutting" below for the rule. Only as a last resort, slightly tighten `line-height` or the entry `margin` in the `<style>` block.

**Problem: content finishes early on page 2 (feels thin)**
Restore the highest-relevance item that was previously cut - a CV that ends high on page 2 looks incomplete.

## ATS Parseability

Most employers run CVs through an ATS before a human sees them, and the ATS reads the PDF's embedded **text layer**, not the rendered page. The HTML pipeline produces a clean single-column text layer, but still verify it after the layout passes the compile-and-inspect loop:

```bash
pdftotext -layout cv/main_<company>.pdf cv/main_<company>.txt
```

`pdftotext` comes from [poppler](https://poppler.freedesktop.org/) and is an **optional** dependency. If it is not installed, skip the mechanical check with a warning and rely on the visual PDF read for keyword coverage.

What to check in the extraction:

- **Contact details as literal text.** The email and phone must appear as printed text in the extraction. The failure mode is a contact detail carried *only* by a hyperlink (like the `LinkedIn` link text, whose URL is not in the text layer): invisible to an ATS. The template prints the LinkedIn handle as visible text for exactly this reason.
- **No garbled output.** `(cid:NNN)` markers or `�` characters mean a font is embedded without a Unicode mapping - an ATS sees the same garbage. The stock Helvetica/Arial setup extracts cleanly.
- **Reading order.** The single-column HTML template extracts in visual order. The `entryhead` table has role/org in the first cell and location/dates in the second, so a role line reads before its dates - correct order.
- **Keyword coverage.** Match the posting's required/preferred terms against the extracted text, in the posting's language. Prefer the posting's exact term over a synonym when it is truthfully applicable - ATS matching is often literal. Never add a keyword the profile does not support.

## Page Budget - Hard 2-Page Limit

The CV **must** fit on exactly 2 pages when rendered. Use these content limits as a guide:

| Section | Max budget |
|---------|-----------|
| Profile statement | 3-4 lines |
| Core Competencies | 5-7 items, each 1-2 lines |
| Most recent role | 4-5 bullets |
| Previous role | 2-3 bullets |
| Older roles | 1-2 bullets (1 line each) |
| Education | 2-4 entries |
| Publications | 2-3 entries |
| Awards | 3 entries, single line each |
| References | "Available upon request." (single line) |

**If in doubt, cut rather than squeeze.** Shrinking the font-size or margins to force-fit content makes the CV look cramped.

## Relevance-weighted cutting (the right way to shrink a CV)

**Cut by signal, not by section.** Static priority lists ("remove oldest education first, then shorten the earliest role...") are wrong when a relevant "lower-priority" item is competing with an irrelevant "higher-priority" item. An older-role bullet that speaks directly to the posting is worth more than a recent-role bullet that does not.

For every candidate line, score three things:

1. **Relevance to THIS posting** — does the line hit a named tool, keyword, or stated responsibility in the job ad?
2. **Uniqueness** — is it the only place this claim appears, or is it duplicated elsewhere in the CV?
3. **Narrative load** — does the cover letter depend on it? If cutting the line would force you to rewrite a cover-letter paragraph, it is load-bearing.

Cut the lowest-total-score line first, regardless of which section it sits in.

### Practical order of cuts (easiest → last resort)

1. **Redundancy.** If an achievement appears in both Core Competencies AND a role bullet, the Core Competencies version is usually the cleaner cut (the experience bullet is more concrete evidence).
2. **Profile-statement fluff.** A sentence that just restates what Publications or Skills will show. ("Peer-reviewed publications on X..." is already a Publications entry — profile can claim it once and stop.)
3. **Low-relevance experience bullets.** A bullet about work that does not touch posting keywords, wherever it sits. This cuts across sections before touching the structural list.
4. **Low-relevance supporting content.** An older-role bullet that does not speak to the target role. A certification that does not touch the posting's stack. A language entry that can be condensed to one line.
5. **Low-relevance publications.** Keep 1-2 publications that best match the posting. Cut the rest before touching experience bullets.
6. **Last-resort structural cuts.** Oldest education entry, tightening an older role to 1-2 bullets, collapsing Certifications into a single line. These only happen if the relevance-weighted cuts above have already been exhausted.

### Pitfalls to avoid

- Do not mechanically cut from the bottom of a static section list without checking relevance. "Cut the oldest role first" is wrong if that role is literally about the skill the posting asks for.
- Do not cut the one concrete example the cover letter leans on. Relevance is measured against the cover letter you wrote, not just the job posting — interviewers will have read both.
- Do not cut to fit if the fit is borderline (2.05 pages). Prefer trimming a single low-relevance line or slightly tightening `line-height` in the `<style>` block for near-misses; reserve larger content cuts for genuine overflow (real content on page 3, not just a single trailing line).

## Recommended Section Order

The section order varies by role type:

**For technical / data science / ML roles:**
1. Profile statement / elevator pitch
2. Core Competencies / Skills
3. Professional Experience (reverse chronological)
4. Education (reverse chronological)
5. Certifications
6. Languages
7. Publications & Awards
8. References

**For domain-specific / specialist roles:**
1. Profile statement / elevator pitch
2. Core Competencies / Skills
3. Education (reverse chronological) - credentials are a key qualifier
4. Professional Experience (reverse chronological)
5. Publications & Awards
6. References
