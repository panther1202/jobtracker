# Custom Templates

This folder holds user-registered HTML templates, managed by the `/add-template` command. The framework works out of the box with its stock HTML templates (`cv/main_example.html` for CVs, `cover_letters/cover_example.html` for cover letters), rendered to PDF by `tools/render_pdf.py` — this folder only gets content when you register your own.

## Layout

```
templates/
├── cv/
│   └── <template-name>/
│       ├── template.html    # Profile-agnostic skeleton ([PLACEHOLDER] tokens)
│       ├── TEMPLATE.md      # Manifest: page limit, fonts, style rules, pitfalls
│       └── styles.css       # Optional external stylesheet (usually inlined in a <style> block instead)
└── cover_letters/
    └── <template-name>/
        └── (same layout)
```

CSS is most reliable when inlined in a `<style>` block inside `template.html`; images and fonts are safest embedded as data URIs, since the renderer has limited support for external assets.

## How it works

- `/add-template` interviews you for the template's instructions (fonts, style rules, page limit), stores the files here, and runs a mandatory test render before registering anything.
- Activating a template adds a managed block to `05-cv-templates.md` or `06-cover-letter-templates.md`, which is what `/apply` reads when drafting — no other wiring needed.
- `/add-template --list` shows registered templates; `/add-template --use <name>` switches; `/add-template --use default` reverts to the stock templates.

Templates are stored with `[PLACEHOLDER]` tokens instead of personal data, so they are safe to commit and share.
