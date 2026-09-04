# Candidate Profile

<!-- SETUP: This file is populated by running /setup -->
<!-- After running /setup, all sections will be filled with your actual information -->

## Identity
- **Name:** Panth Patel
- **Location:** Somerset, NJ, USA. Job search targets US market (Somerset, NJ / NYC metro / remote / nationwide).
- **Phone:** +1 732-649-0368
- **Email:** panthpatel.aiengg@gmail.com
- **LinkedIn:** https://www.linkedin.com/in/panthpatel0122/
- **GitHub:** N/A
- **Languages:** English (fluent), Hindi (fluent), Gujarati (fluent)
- **Status:** Employed - Software Engineer at Sunflower Labs
- **Constraints:** None (open to relocation and remote); already based in the US, so no relocation lead time affects start dates

## Education

| Degree | Period | Institution | Key Topics |
|--------|--------|-------------|------------|
| Post Graduate Diploma, Software Development - AI | 2024-2025 | Algonquin College (Ottawa, ON) | AI/ML application development |
| Post Graduate Diploma, Project Management | 2023-2024 | Fleming College (Peterborough, ON) | Project management |
| Bachelor's, Computer Science and Engineering (CSE) | 2020-2023 | Indus University | Computer science and engineering |
| Undergraduate Diploma, Computer Science | 2017-2020 | L.J. Polytechnic | Computer science fundamentals |

**Certifications:** Certified Associate in Project Management (CAPM)(R)

## Professional Experience

### Software Engineer - Sunflower Labs (Feb 2026 - Present)
Remote (US) - works remotely from Somerset, NJ, USA; Sunflower Labs is based in Vadodara, Gujarat, India

Two concurrent tracks. Lead with whichever the target posting calls for (see Positioning below).

**(A) Applied AI / LLM automation**
- Python developer on the AI team, building AI tools for clients and integrating AI into existing products for AI compliance
- Independently developing a tool that reads large IONM (Intraoperative Neuromonitoring) machine JSON output and converts it into CMS 1500 format for insurance claim submission, using Python + Amazon Nova v1 Pro on Amazon Bedrock (in development, not production)
- Cut manual claim-form entry from roughly one full day per surgery to under 5 minutes; extraction accuracy currently 85% and improving (measured informally; no formal eval harness)
- Owns prompt design, structured-output extraction, and field-level validation against expected values

**(B) Full-stack engineering on a multi-tenant healthcare SaaS patient-engagement platform (client engagement)**

NDA: **never name the client or its EMR/practice-management vendors.** Describe as "a multi-tenant healthcare SaaS patient-engagement platform" and "a third-party EMR". Never cite internal ticket/epic IDs.

- Schema-per-tenant PostgreSQL on AWS ECS. Owns features end-to-end across ~11 repositories: data model, raw-SQL multi-tenant migration, FastAPI backend, workflow-engine logic, React UI, tests, QA sign-off
- Stack: Python 3.11, FastAPI, async SQLAlchemy 2.0 / SQLModel, Pydantic, asyncpg, PostgreSQL; React 18 + TypeScript, Vite, Redux Toolkit, React Query, Radix/Tailwind, AG Grid, FullCalendar; AWS Lambda, SNS/SQS (FIFO), S3; Inngest durable workflows; Mirth Connect (HL7); pytest/pytest-asyncio, vitest
- **Patient self-service appointment reschedule:** DOB identity gate with lockout and anti-enumeration responses, JWT session tokens, a pure slot-availability engine (recurrence expansion, timezone/DST-safe local/UTC conversion, rolling 30-day horizon), and a concurrency-safe confirm path using `SELECT ... FOR UPDATE` plus PostgreSQL advisory locks for one-winner booking (409 on race). Shipped the patient React wizard mock-first so frontend and backend landed in parallel
- **Cross-flow identity voucher:** designed a device-bound, patient-scoped JWT voucher so patients skip DOB re-verification between portals; rejected a simpler server-side "recent verify by patientId" design that would have let any holder of a bearer link bypass the identity gate
- **Workflow serialization / race-condition repair:** diagnosed that Inngest `concurrency=1` does not serialize suspended executions (the slot is released at `wait_for_event`), so one inbound SMS reply resumed only one of several parked workflows. Built per-patient ownership locking with a FIFO grant queue and TTL-based crash self-healing (no polling cron), with a pure decision core under unit test; later found and fixed a lost-grant race by making the DB owner row the source of truth and the event merely a fast wake
- **Workflow chronology fixes:** traced a double-applied delay across serializer and engine (a 5-minute buffer firing at 10) and a reply-attribution race caused by writing conversation state after the physical send; verified fixes with a deterministic in-process harness (fake step + mocked storage) instead of live sends on shared infrastructure
- **Multi-channel delivery status (SMS / Email / Voice):** JSONB `channelDelivery` column plus expansion API; channel-aware dashboard with live polling and a voice-call detail page; voice/TTS configuration panel with readability validation that blocks publish on unreadable scripts
- **Broadcast automation:** designed and built a one-time, CSV-driven mass-messaging feature end-to-end - data model, S3 CSV pipeline, engine scheduler + executor, 5-step wizard, dashboard, permissions, migrations, and a 45-case QA matrix - deliberately reusing existing campaign/workflow primitives instead of reviving parked code
- **Bi-directional EMR integration:** inbound case / insurance / appointment sync over SNS to SQS FIFO to Mirth to REST, plus outbound form-approval push. Fixed insurance round-trip identity with an `externalId` backbone (replacing fragile array-index and policy-number matching), E.164 phone normalization at a single correct boundary, timezone-bucketed practice-line routing, provider de-duplication by EMR provider ID across every appointment-creation source, and automated case-note write-back on message delivery with a three-column dedupe key
- **Calendar blackouts:** surfaced availability blackouts on the staff FullCalendar as background events and blocked drag / resize / manual reschedule into them, reusing the patient-side slot engine's recurrence and timezone logic rather than duplicating it
- **QA & release engineering:** ran structured QA rounds, produced Excel test-case matrices, triaged bugs against intent (withdrew an invalid bug after confirming the ticket description itself was wrong), maintained a standalone pytest end-to-end automation harness (workflows, campaigns, webhooks, delivery verification)

### Teacher - Aarham Academy (Feb 2023 - Jul 2023)
Ahmedabad, Gujarat, India
- Taught mathematics and science to students through 10th grade for 6 months, concurrent with the final semester of the Bachelor's degree

### Python Intern - InfoLabz (Jun 2021 - Aug 2021)
- Python development internship, 2 months

### QA Tester - Sunflower Labs (Aug 2020 - Dec 2020)
- Worked as a QA tester during the break between undergraduate diploma and Bachelor's degree

### Core BOD (Volunteer Leadership) - Rotaract Club of Indus University (Mar 2021 - Jul 2023)
Ahmedabad, Gujarat, India
- Led Corporate Social Responsibility (CSR) initiatives as a Core BOD member, coordinating with external sponsors, concurrent with undergraduate studies

## Independent Projects

Verified against the local repositories under `C:\Users\panth\Projects` on 2026-09-04.

- **Loan Default AI Layer** (2026, in progress - `Projects/Loan Default Prediction`): AI-engineering layer over a frozen scikit-learn LogisticRegression (26 features). TypeScript deterministic decision + attribution core, parity-tested against the Python pipeline; ECOA protected attributes (Age, marital status) filtered out of every LLM-facing explanation in code, not in the prompt; nine architecture decision records; target stack Cloudflare Workers with Gemini through Cloudflare AI Gateway. **Stage 1a only is built. The RAG/retrieval stage is designed but not implemented** - never describe this project as having RAG.
- **GateKeep** (2026 - `Projects/GateKeep`): Python + Streamlit LinkedIn auto-poster with a human-approval gate. Google Gemini 2.5 Flash drafting grounded in verified facts, banned-buzzword flagging, LinkedIn OAuth 2.0 Posts API, headless scheduled publisher, pytest suite (queue, generation, publish, LinkedIn). Confirmed working: real generated posts in `posts.json`, git history shows live-API fixes.
- **Loan Default Prediction** (2025 - `Projects/Loan Default Prediction`, `Projects/Loan prediction`): Python pipeline comparing logistic regression, random forest, gradient boosting, KNN, naive Bayes and SVM, scored on **precision, recall, F1 and ROC-AUC** with one-hot encoding and feature scaling; served for inference through a **Flask** REST API (`Projects/Loan System`). This is what the "Loan Qualification Engine" note in CLAUDE.md refers to.
- **Histogram** (Jan 2025 - `Projects/Histogram`): **Flask** + OpenCV web tool clustering image pixels with DBSCAN, K-means and mean shift to find user-defined color patterns; image upload, masking, CSV export. **Co-authored with Saumya Ramoliya** - always say "built with one collaborator", never imply solo work.
- **Image Color-Pattern Clustering Tool** (Apr 2024 - Sep 2024, freelance client - `Projects/sample`): Python + OpenCV clustering tool identifying user-defined color patterns in images. Reached 70% completion before the client discontinued the engagement prior to deployment. **On CVs, state what was built and omit the completion percentage** - Panth's call (2026-08-19); it is honest to omit, but never claim it shipped. Distinct from Histogram; never merge the two.
- **Holiday Notification Service** (academic coursework): scheduled notification engine built with FastAPI and Firebase. *Dates, institution and scope still unconfirmed - ask Panth before claiming any detail.*

**Not resume material:** `Projects/jobtracker` is a fork of MadsLorentzen/ai-job-search, not original work. `Projects/Project brainstorming` is an Obsidian vault. `Projects/Loan prediction` and `Projects/sample` are superseded earlier versions.

## Positioning (dual-track)

Two credible tracks; pick per posting rather than averaging them.

- **AI / LLM engineer** - lead with the Bedrock IONM to CMS 1500 pipeline, LangChain/LangGraph, prompt and output-validation work. Backend depth from the SaaS platform becomes supporting evidence of production engineering.
- **Backend / full-stack engineer** - lead with the multi-tenant healthcare SaaS platform: FastAPI + async SQLAlchemy, PostgreSQL concurrency control, event-driven AWS, React 18/TS, race-condition debugging. The LLM pipeline becomes one bullet showing AI fluency.

For generalist SWE or platform roles, favour the backend track: more production surface, more systems depth, clearer scale.

## Technical Skills

### Programming & ML
- **Python** (Advanced/Proficient - performs tasks independently, handles complex situations, troubleshoots effectively): LangChain, LangGraph, Hugging Face Transformers, Scikit-learn, Keras, TensorFlow, PyTorch, OpenCV
- **JavaScript / TypeScript** (Advanced/Proficient) - including **React**; current work stack is React/TypeScript, hands-on front-end and full-stack
- **SQL** (Advanced/Proficient)
- **Model evaluation** - classifier comparison scored on precision, recall, F1 and ROC-AUC (loan projects); parity testing a TypeScript scoring core against its Python reference. LLM accuracy on the Bedrock pipeline is tracked informally against expected output - **never call this an eval framework or regression harness**

### Backend / data
- **FastAPI** (good experience - building/serving APIs for Python services), async SQLAlchemy 2.0 / SQLModel, Pydantic, asyncpg
- **Flask** - REST API serving an ML model (`Projects/Loan System`) and an OpenCV web tool (`Projects/Histogram`). Personal/academic, not production
- **PostgreSQL** - advisory locks, `SELECT ... FOR UPDATE`, JSONB modeling, partial-unique indexes, `search_path` semantics; idempotent multi-tenant raw-SQL migrations
- REST API design; pytest / pytest-asyncio with mock-session fixtures

### Frontend
- React 18 + TypeScript, Vite, Redux Toolkit, React Query (state-boundary judgement), Radix + Tailwind design-system compliance, AG Grid, FullCalendar, ReactFlow, vitest
- Multi-step wizard architecture with aggregated cross-field validation; mock-driven frontend delivery ahead of backend

### Distributed / event-driven
- Inngest durable workflows and their concurrency semantics, race-condition diagnosis and repair, FIFO ordering, idempotency via natural-key upserts, crash recovery via TTL self-healing, SNS / SQS / Lambda pipelines, DLQ and poison-message reasoning

### Multi-tenancy & security
- Schema-per-tenant isolation and its failure modes, JWT session and voucher design, anti-enumeration response design, lockout and rate-limit gating, token entropy trade-offs, tenant-context correctness in background jobs

### Integrations
- Mirth Connect channel development, HL7 intake, EMR data-contract reverse-engineering from real payloads, AWS SDK / IAM debugging, CSV bulk-ingestion pipelines

### LLM / agentic
- **LLM providers / APIs** (hands-on across multiple): OpenAI, Amazon Bedrock (Amazon Nova v1 Pro), Google AI Studio (Gemini); comfortable choosing and switching between models
- **LLM tool/function-calling** (used within LangGraph pipelines)
- **MCP (Model Context Protocol)** - hands-on building and integrating multiple MCP servers/tools into development workflows; actively exploring new MCPs to speed up development
- Prompt engineering, structured-output design and schema validation, output validation that catches a wrong response at the field

### Known gaps (recurring in AI job postings - never claim these)
LLM fine-tuning; production RAG (chunking, hybrid search, reranking); vector databases; LlamaIndex, Semantic Kernel, AutoGen; knowledge graphs; GCP / Vertex AI; Azure; Kubernetes; Django; Kafka / Pub/Sub; MLflow, Langfuse, RAGAS, TruLens; FHIR (HL7 v2 yes, FHIR no); Next.js. No Master's degree (two Post Graduate Diplomas). n8n and other iPaaS platforms: not hands-on as of 2026-09-04 - see the n8n memory note before answering an iPaaS question.

### Domain Expertise
- Adaptable across domains, eager to learn
- US healthcare - patient engagement, insurance and eligibility data models, Workers' Comp and Auto claim fields, TCPA quiet-hours compliance, SMS/voice/email delivery semantics, appointment lifecycle and reschedule rules, timezone/DST correctness in clinical scheduling; IONM data and CMS 1500 claims automation
- Applied AI/ML - prompt engineering, AI-compliance engineering

### Engineering practice
- Spec/plan-first delivery, behavior-preserving refactors (extract shared services verbatim before reuse), pure-function cores for testability, cross-team API contract coordination, deliberate scope-cutting with documented rationale

### Software & Tools
- IDEs: VS Code, IntelliJ
- Cloud/Infra: AWS (ECS, Lambda, SNS, SQS, S3, Bedrock), Docker, Git
- Databases: PostgreSQL, DynamoDB
- Other: Testing, debugging, Claude Code as an agentic coding assistant

## Publications
None

## Awards
None

## References
- Yash Patel, CTO/VP, Sunflower Labs (current manager) - yash@thesunflowerlab.com, https://www.linkedin.com/in/yash-patel/

More references available upon request.
