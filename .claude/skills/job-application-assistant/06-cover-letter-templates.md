# Cover Letter Templates and Tailoring Guide

## Template: HTML rendered to PDF

Cover letters are written as a single self-contained HTML file and rendered to PDF with `tools/render_pdf.py` (xhtml2pdf / the `pisa` library, pure Python, no TeX to install). Bullets use the same body font automatically, so there is no font-mismatch pitfall to work around.

**Output file:** `cover_letters/cover_<company>_<role>.html` (the renderer writes the `.pdf` alongside it)
**Render with:** `python tools/render_pdf.py`
**Master reference:** `cover_letters/cover_example.html` (the tracked template with `[PLACEHOLDER]` tokens; `/setup` fills the tokens and `/apply` copies this structure into `cover_letters/cover_<company>_<role>.html` and tailors it per role)

### Render command

```bash
python tools/render_pdf.py cover_letters/cover_<company>_<role>.html
```

The script prints `OK  <path>` on success and `FAILED  <path>` on error. It does **not** report a page count, so you must open the rendered PDF with the Read tool and count the pages yourself. Any page count other than 1 is a failure that must be fixed before presenting to the user.

### Renderer capabilities and limits

xhtml2pdf supports a practical subset of HTML/CSS. Stay inside it: `@page { size: letter; margin: ... }`, standard block/inline CSS, `<ul>/<li>`, colors, borders, `font-size` in `pt`, `line-height`, and `text-align` all work. Flexbox, CSS grid, and advanced modern CSS do not. Do not invent CSS the renderer cannot do; ground every change in the patterns already present in `cover_letters/cover_example.html`.

## Compile-and-Inspect Loop (MANDATORY)

After writing the cover letter and before presenting to the user, always render and visually inspect the PDF. Iterate until the layout is clean:

1. Run `python tools/render_pdf.py cover_letters/cover_<company>_<role>.html`
2. Confirm the script printed `OK`
3. Read the rendered `.pdf` via the Read tool and count pages: must be exactly 1
4. Visually check: the signature block fits with the body (never overflows to a second page), no text is cut off, and the bullets read in the same font as the paragraphs

If the letter spills onto a second page, cut body text (see the word budget below) or, as a last resort, slightly tighten `line-height` or the paragraph `margin` in the `<style>` block. Do not shrink the font to hide overflow.

## Document Structure

The cover letter is one HTML file. The `<style>` block defines the look; the `<body>` holds the header, date, paragraphs, one bullet block, and the signature. This is the skeleton (see `cover_letters/cover_example.html` for the full template):

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@page { size: letter; margin: 1.7cm 1.8cm; }
body { font-family: Helvetica, Arial, sans-serif; font-size: 10.5pt; color: #222; line-height: 1.4; }
h1 { color: #2b6cb0; font-size: 22pt; margin: 0 0 2pt 0; }
.contact { font-size: 9.5pt; color: #444; margin-bottom: 4pt; }
.contact a { color: #2b6cb0; text-decoration: none; }
.rule { border-bottom: 1.2pt solid #2b6cb0; margin-bottom: 12pt; }
.date { color: #555; margin-bottom: 12pt; font-size: 9.5pt; }
p { margin: 0 0 9pt 0; text-align: justify; }
ul { margin: 0 0 9pt 0; padding-left: 16pt; }
li { margin-bottom: 3pt; text-align: left; }
.label { font-weight: bold; }
.sig { margin-top: 14pt; }
</style>
</head>
<body>

<h1>[YOUR NAME]</h1>
<div class="contact"><a href="mailto:[YOUR_EMAIL]">[YOUR_EMAIL]</a> &nbsp;|&nbsp; <a href="[YOUR_LINKEDIN_URL]">LinkedIn</a></div>
<div class="rule"></div>

<div class="date">[DATE]</div>

<p>Dear [Hiring Manager / named person],</p>

<p>[Opening paragraph]</p>

<p>[Body paragraph, then the bullets:]</p>
<ul>
<li><span class="label">[Label]:</span> [Achievement]</li>
<li><span class="label">[Label]:</span> [Achievement]</li>
<li><span class="label">[Label]:</span> [Achievement]</li>
</ul>

<p>[Why this company specifically]</p>
<p>[Personal fit paragraph]</p>
<p>I look forward to hearing from you.</p>

<p class="sig">Kind regards,<br>[YOUR NAME]</p>

</body>
</html>
```

### The style conventions (what each class does)

- **`h1`** is the candidate name, blue (`#2b6cb0`) at 22pt.
- **`.contact`** is a single line under the name: email (as a `mailto:` link) and LinkedIn, separated by `|`.
- **`.rule`** is the blue horizontal divider under the header.
- **`.date`** is the letter date.
- **`<p>`** paragraphs are justified body text with consistent bottom spacing.
- **`<ul>`** is the single bullet block; bullets lead with a bold `<span class="label">` and use the same body font automatically.
- **`.sig`** is the signature block ("Kind regards," + name), with extra top margin.

## Tailoring Guidelines

### Salutation
- If you know the hiring manager's name: "Dear [First Last],"
- If you know the team: "Dear [Company] hiring team,"
- Generic: "Dear Hiring Manager," (avoid "To whom it may concern")

### Length - Hard 1-Page Limit
- Target: 1 page including signature block
- Maximum: **never exceed 1 page**
- **Word budget: 250-300 words** of body text (not counting HTML markup). This is the safe maximum. 350 words will overflow.
- **Always count the blocks**: opening paragraph + body/bullet paragraph + company paragraph + fit paragraph. When adding company-specific content, trim other content to compensate rather than adding net length.

### Forward-Looking Framing
- Lead the opening with a concrete achievement, not "I am early in my career"
- Frame experience as what you will solve for *them*, not just what you did before
- Reference the specific company's mission, product, or a verified fact about them
- Acknowledge any genuine stack/skill gap honestly and confidently, framing the ramp rather than hiding it

### Bullet Style
- One `<ul>` block, 3-5 bullets, is ideal
- Start each bullet with a bold `<span class="label">Label:</span>` or an action verb
- Put a number in the bullet wherever possible
- Bullets inherit the body font automatically - no special handling needed

### AI Tooling
- If you reference AI coding tools, mention **Claude Code** by name

### Non-English Cover Letters
- Same template structure, just write the content in the posting's language
- Adjust the date format to local convention
- Adjust the closing to local convention (e.g. "Med venlig hilsen," for Danish)

## Checklist Before Finalizing
- [ ] No em-dashes (use commas or periods instead)
- [ ] No cliches or empty filler
- [ ] Every claim backed by a specific example
- [ ] Forward-looking framing: focuses on tasks you'll solve, not just past duties
- [ ] Motivation paragraph references this specific company's mission/values (verified)
- [ ] Company name and role are correct throughout
- [ ] Date is current
- [ ] Renders to exactly one page (verified by reading the PDF)
- [ ] Language matches the job posting language
- [ ] Salutation is appropriate (named person if possible)
- [ ] Opening is engaging and specific, not generic

## Submission Guidelines (Best Practice)
- Submit only the documents the employer requests
- The rendered PDF preserves formatting; submit the `.pdf`, not the `.html`
- Name files clearly: "[Your Name] CV" and "[Your Name] Cover Letter"
- Follow all employer instructions regarding anonymity or specific materials
