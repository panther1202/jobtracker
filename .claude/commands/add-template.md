# /add-template - Register a Custom CV or Cover Letter Template

You are helping the user register their own HTML template with the AI Job Search framework. The framework ships with stock HTML templates (`cv/main_example.html` for CVs, `cover_letters/cover_example.html` for cover letters), rendered to PDF by `tools/render_pdf.py`. This command lets the user swap in their own HTML template: store the template file, capture usage instructions (style rules, page limits, any embedded assets), verify the template renders, and wire it into the `/apply` workflow so every future application uses it.

`$ARGUMENTS` may contain a subcommand, a file path, or nothing.

Follow these steps **in order**.

---

## Step 0: Parse Arguments

- If `$ARGUMENTS` contains `--list`: run **List Mode** below and stop.
- If `$ARGUMENTS` contains `--use <name>`: skip to **Step 5: Activate** with that template name. `--use default` deactivates any custom template and restores the stock guidance (see Step 5).
- If `$ARGUMENTS` contains a file path or @-mentioned file: treat it as the template source and carry it into Step 1.
- Otherwise: start the registration flow at Step 1.

### List Mode

Use Glob with `templates/**/TEMPLATE.md` to find registered templates. For each, read the manifest and print a table:

```
## Registered Templates

| Name | Type | Page limit | Active |
|------|------|------------|--------|
| <name> | CV / Cover letter | <N> page(s) | yes/no |
```

A template is **active** if `05-cv-templates.md` (CV) or `06-cover-letter-templates.md` (cover letter) contains an `ACTIVE-TEMPLATE` managed block naming it. If no custom templates exist, say so and explain that `/add-template` registers one. Stop here.

---

## Step 1: Template Type and Source

Ask the user (skip anything already answered by `$ARGUMENTS`):

1. **Type:** Is this a **CV** template or a **cover letter** template?
2. **Source:** Where is the template? Accept any of:
   - A path or @-mention of an `.html` file (plus an optional external `.css` file)
   - Pasted HTML content
   - A directory containing the template and its assets (stylesheet, images)

Read every provided file. Remember that `render_pdf.py` supports only a practical subset of HTML/CSS (`@page` for size/margins, standard block/inline CSS, tables, lists, colors, pt font sizes) and **not** flexbox, grid, or advanced CSS. If the template relies on unsupported layout features, flag this to the user — it may not render as designed.

---

## Step 2: Capture Template Instructions

Interview the user for the metadata that `/apply` needs to use the template correctly. Infer as much as possible from the HTML/CSS source first (`@page` size and margins, `font-family` declarations, colors) and present your inferences for confirmation rather than asking blind questions.

Collect:

1. **Name** - short kebab-case identifier (e.g. `awesome-cv`, `classic-serif`). Must not collide with an existing folder in `templates/`.
2. **Fonts** - which font(s) the template uses and where they come from:
   - **System fonts** (declared in CSS `font-family`, e.g. Helvetica, Georgia): record the font stack and note that the renderer relies on fonts available to it; a common, widely available stack is safest.
   - **Embedded fonts** (`.ttf`/`.otf` supplied with the template): these must be embedded as a data URI in a CSS `@font-face` rule (external font file references are unreliable in the renderer). Record which fonts are embedded this way.
3. **Style rules** - anything the drafter must preserve when filling the template: color scheme, section order, heading style, spacing conventions, bullet formatting, date format.
4. **Page limit** - hard page count for the rendered PDF. Default: **2 pages** for a CV, **1 page** for a cover letter. `/apply`'s render-and-inspect loop enforces this.
5. **Bundled assets** (optional) - any images or fonts the template needs. Because xhtml2pdf has limited support for external assets, these are safest embedded as data URIs (images) or `@font-face` data URIs (fonts) directly in the HTML/CSS.
6. **Known pitfalls** (optional) - CSS the renderer does not support (flexbox/grid), content that breaks the layout, sections that must not be reordered.

---

## Step 3: Store the Template

Create the template folder:

- CV: `templates/cv/<name>/`
- Cover letter: `templates/cover_letters/<name>/`

Write into it:

1. **`template.html`** - the template skeleton. Replace all personal data in the source with `[PLACEHOLDER]` tokens (`[YOUR_NAME]`, `[YOUR_EMAIL]`, `[YOUR_PHONE]`, `[YOUR_LINKEDIN_URL]`, ...) so the template is shareable and profile-agnostic. Keep the structure, markup, and styling exactly as provided.
2. **Stylesheet** - if the template uses an external `.css` file, store it alongside `template.html`. Note that inlining the CSS into a `<style>` block in `template.html` is more reliable for the renderer than an external stylesheet reference; prefer inlining when practical.
3. **Assets** - embed any bundled images or fonts as data URIs directly in `template.html` (or the stylesheet). Avoid external asset references, which xhtml2pdf handles unreliably.
4. **`TEMPLATE.md`** - the manifest. Use exactly this format:

```markdown
# Template: <name>

- **Type:** CV | Cover letter
- **Page limit:** <N> page(s)
- **Fonts:** <main font stack> (<system fonts | embedded via @font-face data URI>)
- **Assets:** <images/fonts embedded as data URIs, or "none">

## Render command

    python tools/render_pdf.py <output dir>/<file>.html

## Style rules

- <rule 1: colors, section order, heading style, ...>
- <rule 2>

## Known pitfalls

- <pitfall and its fix, or "none recorded">
```

---

## Step 4: Verify the Template Renders (MANDATORY)

Never register a template without a successful test render. HTML templates that "look fine" in source routinely rely on CSS the renderer does not support (flexbox/grid), overflow the page limit, or fail on external asset references.

1. Copy `template.html` to a scratch file in the same folder (e.g. `_render_test.html`) and fill every `[PLACEHOLDER]` with realistic dummy data (name, contact line, one education entry, one job entry with 3 bullets — enough content to exercise the layout).
2. Render with `render_pdf.py`:
   ```bash
   python tools/render_pdf.py templates/<type>/<name>/_render_test.html
   ```
3. If the render fails or looks wrong: show the user the relevant error output, diagnose (unsupported CSS, external asset that should be inlined, overflow), fix what you can (inline the CSS, embed assets as data URIs, simplify unsupported layout), and re-render. If the fix needs input only the user has (a missing font file, a license-restricted asset), ask for it and wait.
4. On success, Read the produced PDF and confirm the layout renders sensibly (no overlapping text, fonts loaded, page count within the declared limit for dummy content). Record any surprises in the manifest's "Known pitfalls".
5. Delete the scratch files: `_render_test.html` and `_render_test.pdf`. (There are no `.aux`/`.log`/`.out` artifacts to clean.)

Do not proceed to Step 5 until the test render passes.

---

## Step 5: Activate the Template

Activation wires the template into `/apply` by adding a **managed block** to the top of the relevant guidance file — `05-cv-templates.md` for CVs, `06-cover-letter-templates.md` for cover letters. `/apply` reads these files in its drafting step, so the block is all it takes.

Insert (or replace, if one exists) this block immediately after the file's H1 title:

```markdown
<!-- BEGIN ACTIVE-TEMPLATE (managed by /add-template - do not edit by hand) -->
> **Active template override: `<name>`**
>
> A custom template is active. Where this block conflicts with the stock guidance below, this block wins. Structural advice below (tailoring, page-budget, cutting rules) still applies.
>
> - **Template skeleton:** `templates/<type>/<name>/template.html` — use this as the structural reference instead of the stock template
> - **Manifest:** `templates/<type>/<name>/TEMPLATE.md` — read this for style rules and known pitfalls before drafting
> - **Render with:** `python tools/render_pdf.py <file>.html`
> - **Fonts:** <font summary, including any @font-face data-URI note for embedded fonts>
> - **Page limit:** exactly <N> page(s)
> - **Output file:** unchanged (`cv/main_<company>.html` / `cover_letters/cover_<company>_<role>.html`); embed any assets the template needs as data URIs rather than referencing external files
<!-- END ACTIVE-TEMPLATE -->
```

Rules:

- Exactly **one** managed block per guidance file. Replace the whole block between the `BEGIN`/`END` markers when switching templates; never stack blocks.
- **`--use default`**: remove the managed block entirely. The stock HTML template guidance below it is untouched and takes over again.
- Do not modify anything outside the markers.

---

## Step 6: Confirm

Present a summary:

> **Template `<name>` registered and activated.**
>
> - Files: `templates/<type>/<name>/` (skeleton, manifest<, stylesheet>)
> - Test render: passed with `render_pdf.py` (<N> page(s))
> - `/apply` will now draft <CVs | cover letters> from this template.
>
> Useful follow-ups:
> - `/add-template --list` — see all registered templates
> - `/add-template --use <other-name>` — switch templates
> - `/add-template --use default` — go back to the stock HTML template

---

## Design Principles

- Registration is idempotent: re-running with the same name offers to update the existing template rather than duplicating it.
- Templates are stored profile-agnostic (`[PLACEHOLDER]` tokens) so they can be shared or committed without leaking personal data.
- The render check in Step 4 is non-negotiable — a template that has never rendered will fail mid-`/apply`, which is the worst place to discover it.
- Activation is a small managed block, not a rewrite of the guidance files: `/setup` and manual edits to `05`/`06` survive template switches, and `--use default` is a clean revert.
