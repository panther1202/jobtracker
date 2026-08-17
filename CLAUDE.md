# Job Application Assistant for Panth Patel

<!-- SETUP: This file is populated by running /setup -->
<!-- After running /setup, all [PLACEHOLDER] tokens will be replaced with your actual information -->

## Role
This repo is a job application workspace. Claude acts as a career advisor and application assistant for Panth Patel, helping with:
1. **Job fit evaluation** - Assess job postings against your profile (skills, experience, behavioral traits)
2. **CV tailoring** - Adapt existing HTML CV templates to target specific roles
3. **Cover letter writing** - Draft targeted cover letters using existing HTML templates
4. **Interview preparation** - Prepare answers, questions, and talking points for interviews
5. **Career strategy** - Advise on positioning and personal branding

## Candidate Profile

<!-- This section is auto-populated by /setup. You can also fill it in manually. -->

### Identity
- **Name:** Panth Patel
- **Phone:** +1 732-824-1460 (use on all CVs and cover letters)
- **Location:** Currently Vadodara, Gujarat, India; relocating to Somerset, NJ, USA within ~2 months. No commute/relocation constraints; job search targets US market.
- **Languages:** English (fluent), Hindi (fluent), Gujarati (fluent)
- **Status:** Employed - Software Engineer at Sunflower Labs
- **LinkedIn headline:** "AI/Python Engineer | LLM Automation (LangChain, AWS Bedrock) | Building AI tools @ Sunflower Labs"

### Education
<!-- List your degrees, most recent first -->
- **Post Graduate Diploma in Software Development - AI** (2024-2025) - Algonquin College, Ottawa, ON
- **Post Graduate Diploma in Project Management** (2023-2024) - Fleming College, Peterborough, ON
- **Bachelor's in Computer Science and Engineering (CSE)** (2020-2023) - Indus University
- **Undergraduate Diploma in Computer Science** (2017-2020) - L.J. Polytechnic

### Professional Experience
<!-- List your roles, most recent first -->
- **Software Engineer** (Feb 2026 - Present) - **Sunflower Labs** (Vadodara, India; remote-eligible)
  - Two tracks of work: (A) applied AI / LLM tooling, (B) full-stack product engineering on a client SaaS platform. Both are current; emphasise whichever the target posting calls for (see "Positioning" below).

  **(A) Applied AI / LLM automation**
  - Python developer on the AI team, building AI tools for clients and integrating AI into existing products for AI compliance
  - Independently developing a tool that converts large IONM machine JSON output into CMS 1500 insurance-claim format, using Python + Amazon Nova v1 Pro on Amazon Bedrock (in development, not production)
  - Cut manual claim-entry time from ~1 day/surgery to under 5 minutes; current accuracy 85% and improving (measured informally; no formal eval harness)

  **(B) Full-stack engineering on a multi-tenant healthcare SaaS patient-engagement platform (client engagement)**
  - NDA: **never name the client or its EMR/practice-management vendors.** Describe as "a multi-tenant healthcare SaaS patient-engagement platform" and "a third-party EMR". Never cite internal ticket/epic IDs.
  - Schema-per-tenant PostgreSQL, deployed on AWS ECS. Owned features end-to-end across ~11 repositories: data model -> raw-SQL multi-tenant migration -> FastAPI backend -> workflow-engine logic -> React UI -> tests -> QA sign-off
  - Stack: Python 3.11, FastAPI, async SQLAlchemy 2.0 / SQLModel, Pydantic, asyncpg, PostgreSQL; React 18 + TypeScript, Vite, Redux Toolkit, React Query, Radix/Tailwind, AG Grid, FullCalendar; AWS Lambda, SNS/SQS (FIFO), S3; Inngest durable workflows; Mirth Connect (HL7); pytest/pytest-asyncio, vitest
  - **Patient self-service appointment reschedule:** built a DOB identity gate with lockout and anti-enumeration responses, JWT session tokens, a pure slot-availability engine (recurrence expansion, timezone/DST-safe local<->UTC conversion, rolling 30-day horizon), and a concurrency-safe confirm path using `SELECT ... FOR UPDATE` plus PostgreSQL advisory locks for one-winner slot booking (409 on race). Shipped the patient React wizard mock-first so frontend and backend landed in parallel
  - **Cross-flow identity voucher:** designed a device-bound, patient-scoped JWT voucher so patients skip DOB re-verification between portals - rejected a simpler server-side "recent verify by patientId" design that would have let any holder of a bearer link bypass the identity gate
  - **Workflow serialization / race-condition repair:** diagnosed that Inngest `concurrency=1` does not serialize suspended executions (the slot is released at `wait_for_event`), so one inbound SMS reply resumed only one of several parked workflows. Built per-patient ownership locking with a FIFO grant queue and TTL-based crash self-healing (no polling cron), with a pure decision core under unit test; later found and fixed a lost-grant race by making the DB owner row the source of truth and the event merely a fast wake
  - **Workflow chronology fixes:** traced a double-applied delay across serializer and engine (a 5-minute buffer firing at 10) and a reply-attribution race caused by writing conversation state after the physical send; verified fixes with a deterministic in-process harness (fake step + mocked storage) instead of live sends on shared infrastructure
  - **Multi-channel delivery status (SMS / Email / Voice):** JSONB `channelDelivery` column plus expansion API; channel-aware dashboard with live polling and a voice-call detail page; voice/TTS configuration panel with readability validation that blocks publish on unreadable scripts
  - **Broadcast automation:** designed and built a one-time, CSV-driven mass-messaging feature end-to-end - data model, S3 CSV pipeline, engine scheduler + executor, 5-step wizard, dashboard, permissions, migrations, and a 45-case QA matrix - deliberately reusing existing campaign/workflow primitives instead of reviving parked code
  - **Bi-directional EMR integration:** inbound case / insurance / appointment sync over SNS -> SQS FIFO -> Mirth -> REST, plus outbound form-approval push. Fixed insurance round-trip identity with an `externalId` backbone (replacing fragile array-index and policy-number matching), E.164 phone normalization at a single correct boundary, timezone-bucketed practice-line routing, provider de-duplication by EMR provider ID across every appointment-creation source, and automated case-note write-back on message delivery with a three-column dedupe key
  - **Calendar blackouts:** surfaced availability blackouts on the staff FullCalendar as background events and blocked drag / resize / manual reschedule into them, reusing the patient-side slot engine's recurrence and timezone logic rather than duplicating it
  - **QA & release engineering:** ran structured QA rounds, produced Excel test-case matrices, triaged bugs against intent (withdrew an invalid bug after confirming the ticket description itself was wrong), maintained a standalone pytest end-to-end automation harness (workflows, campaigns, webhooks, delivery verification)
- **Teacher** (Feb 2023 - Jul 2023) - **Aarham Academy**
  - Taught math and science to students through 10th grade for 6 months
- **Core BOD (volunteer leadership)** (Mar 2021 - Jul 2023) - **Rotaract Club of Indus University**
  - Led CSR initiatives, coordinating with external sponsors, concurrent with undergraduate studies
- **Python Intern** (Jun 2021 - Aug 2021) - **InfoLabz**
- **QA Tester** (Aug 2020 - Dec 2020) - **Sunflower Labs** (during break between undergraduate diploma and Bachelor's)

### Independent Projects
- **Image Color-Pattern Clustering Tool** (Apr 2024 - Sep 2024, freelance): Python + OpenCV clustering tool to identify user-defined color patterns in images. Reached 70% completion before the client discontinued the engagement prior to deployment.

### Technical Skills
- **Primary:** Python (advanced) - FastAPI, async SQLAlchemy 2.0 / SQLModel, Pydantic, asyncpg; LangChain, LangGraph, Hugging Face Transformers, Scikit-learn, Keras, TensorFlow, PyTorch, OpenCV
- **Backend / data:** PostgreSQL (advisory locks, `SELECT ... FOR UPDATE`, JSONB modeling, partial-unique indexes, `search_path` semantics), idempotent multi-tenant raw-SQL migrations, REST API design, pytest / pytest-asyncio with mock-session fixtures
- **Frontend:** React 18 + TypeScript, Vite, Redux Toolkit, React Query (state-boundary judgement), Radix + Tailwind design-system compliance, AG Grid, FullCalendar, ReactFlow, vitest; multi-step wizard architecture with aggregated cross-field validation; mock-driven frontend delivery ahead of backend
- **Distributed / event-driven:** Inngest durable workflows and their concurrency semantics, race-condition diagnosis and repair, FIFO ordering, idempotency via natural-key upserts, crash recovery via TTL self-healing, SNS / SQS / Lambda pipelines, DLQ and poison-message reasoning
- **Multi-tenancy & security:** schema-per-tenant isolation and its failure modes, JWT session and voucher design, anti-enumeration response design, lockout and rate-limit gating, token entropy trade-offs, tenant-context correctness in background jobs
- **Integrations:** Mirth Connect channel development, HL7 intake, EMR data-contract reverse-engineering from real payloads, AWS SDK / IAM debugging, CSV bulk-ingestion pipelines
- **LLM providers/APIs:** OpenAI, Amazon Bedrock (Amazon Nova v1 Pro), Google AI Studio (multi-provider, comfortable switching models); LLM tool/function-calling in LangGraph
- **Other languages:** JavaScript / TypeScript, SQL
- **Domain:** US healthcare - patient engagement, insurance and eligibility data models, Workers' Comp and Auto claim fields, TCPA quiet-hours compliance, SMS/voice/email delivery semantics, appointment lifecycle and reschedule rules, timezone/DST correctness in clinical scheduling; IONM data and CMS 1500 claims automation
- **Engineering practice:** spec/plan-first delivery, behavior-preserving refactors (extract shared services verbatim before reuse), pure-function cores for testability, cross-team API contract coordination, deliberate scope-cutting with documented rationale
- **Software:** VS Code, IntelliJ, AWS (ECS, Lambda, SNS, SQS, S3, Bedrock), Docker, Git, PostgreSQL, DynamoDB

### Positioning (dual-track)
Two credible tracks; pick per posting rather than averaging them:
- **AI / LLM engineer** - lead with the Bedrock IONM -> CMS 1500 pipeline, LangChain/LangGraph, prompt and output-validation work. Backend depth from the SaaS platform becomes supporting evidence of production engineering.
- **Backend / full-stack engineer** - lead with the multi-tenant healthcare SaaS platform: FastAPI + async SQLAlchemy, PostgreSQL concurrency control, event-driven AWS, React 18/TS, race-condition debugging. The LLM pipeline becomes one bullet showing AI fluency.
For generalist SWE or platform roles, favour the backend track - it has more production surface, more systems depth, and clearer scale.

### Certifications
<!-- List relevant certifications with dates -->
- **Certified Associate in Project Management (CAPM)(R)**

### Publications
None

### Awards
None

### Behavioral Profile
<!-- Your behavioral assessment results (PI, DISC, Myers-Briggs, or self-assessment) -->
- **DISC: Dominance/Influence (D/I) blend** - assertive, results-oriented, sociable
- **Strengths:** Decisiveness, initiative, confidence, energizing others, analytical under pressure
- **Growth areas:** Impatience when decisions stall; benefits from more active listening and deliberate patience
- **Thrives in:** Dynamic, collaborative environments with authority/strategic control, clear communication, and defined expectations; drained by micromanagement and slow decision-making

### What Excites You
<!-- What motivates you professionally -->
- New technical challenges - the best opportunity to learn new tech

### Target Sectors
<!-- Industries and companies you're targeting -->
- Software/AI Engineering: open to any sector, no specific target companies
- Healthcare-adjacent AI applications (natural fit given current project experience)

### Deal-breakers
<!-- Hard constraints on job search -->
None specified

## Repo Structure
- `cv/` - HTML CV variants (rendered to PDF via `tools/render_pdf.py`)
- `cover_letters/` - HTML cover letters (rendered to PDF via `tools/render_pdf.py`)
- `.claude/skills/` - AI skill definitions for the application workflow
- `.agents/skills/` - Job search CLI tools

## Workflow for New Job Applications
1. User provides a job posting (URL or text)
2. **Always evaluate fit first**: skills match, experience match, behavioral/culture match. Present this assessment to the user before proceeding.
3. If good fit: create targeted CV and cover letter inside the application folder `documents/applications/<company>_<role>/`, named `<Full Name> - <Company> - CV.html` and `<Full Name> - <Company> - Cover Letter.html`
4. **Verify both documents** (see Verification Checklist below)
5. Prepare interview talking points based on the role requirements and your strengths

**Important:** When mentioning agentic coding or AI tooling in CVs/cover letters, explicitly reference **Claude Code** by name.

## Verification Checklist
After creating or updating a CV or cover letter, re-read the generated file and verify **all** of the following before presenting to the user. Report the results as a pass/fail checklist.

### Factual accuracy
- [ ] All claims match actual profile (CLAUDE.md / candidate profile) - no fabricated skills, experience, or achievements
- [ ] Job titles, dates, company names, and locations are correct
- [ ] Contact details are correct
- [ ] All company-specific claims (partnerships, products, technology, expansions) have been independently verified via WebFetch/WebSearch - do not trust reviewer agent research without verification

### Targeting
- [ ] Profile statement / opening paragraph is tailored to the specific role (not generic)
- [ ] Skills and experience bullets are reframed to match the job requirements
- [ ] Key job requirements are addressed (with gaps acknowledged where relevant)
- [ ] Nice-to-have requirements are highlighted where there is a match

### Consistency
- [ ] CV follows the standard 2-page HTML format
- [ ] Cover letter follows the established HTML template structure
- [ ] Tone is consistent across CV and cover letter
- [ ] No contradictions between CV and cover letter content

### Quality
- [ ] No HTML syntax errors (balanced tags, and only CSS the renderer supports)
- [ ] No spelling or grammar errors
- [ ] Agentic coding / AI tooling references mention **Claude Code** by name
- [ ] Cover letter is addressed to the correct person (or "Dear Hiring Manager" if unknown)
- [ ] Cover letter fits approximately one page

### Compiled PDF verification (MANDATORY - never skip)
Both documents MUST be rendered to PDF and visually inspected via the Read tool on the PDF output. "Looks fine in the .html" is not acceptable - PDF page-break decisions are unpredictable. Iterate until these all pass:
- [ ] CV and cover letter rendered with `python tools/render_pdf.py <file>.html` (xhtml2pdf, pure Python, no TeX). The `.pdf` is written alongside the `.html`.
- [ ] **CV is exactly 2 pages** - not 1, not 3
- [ ] **No orphaned entry titles** - a job/education title must never sit at the bottom of a page with its bullets spilling to the next page. Keep each role's `.entry` block together; add `page-break-inside: avoid;` to the `.entry` CSS if a break lands awkwardly, and cut low-relevance content to rescue a trailing section that just barely spills
- [ ] **Cover letter is exactly 1 page** - signature block must fit with the body, never overflow
- [ ] **Cover letter fits on one page** with the signature block - trim body content (target 250-300 words) rather than shrinking margins or line-height. The bullet list inherits the body font automatically, so there is no font-mismatch pitfall

### ATS & keyword verification (CV)
ATS parsers read the PDF's embedded text layer, not the rendered page. Extract it with `pdftotext -layout` and verify what a parser sees. `pdftotext` (poppler) is optional - if missing, skip the parseability items with a warning and check keyword coverage from the visual PDF read instead.
- [ ] CV text layer extracts cleanly - no `(cid:*)` markers, `�` replacement characters, or text visible in the PDF but absent from the extraction
- [ ] Email and phone appear as **literal text** in the extraction (icon-glyph noise like `MOBILE-ALT`/`Envelope` is harmless, but a contact detail carried only by an icon or hyperlink is invisible to ATS)
- [ ] Reading order of the extracted text matches the visual order (single-column stock template is safe; multi-column custom templates are where this breaks)
- [ ] Posting keywords covered or honestly absent - synonym-only matches tightened to the posting's exact term where truthfully applicable, keywords the profile genuinely supports added to experience bullets, genuine gaps left visible and **never stuffed**
