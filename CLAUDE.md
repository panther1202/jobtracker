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
  - Python developer on the AI team, building AI tools for clients and integrating AI into existing products for AI compliance
  - Independently developing a tool that converts large IONM machine JSON output into CMS 1500 insurance-claim format, using Python + Amazon Nova v1 Pro on Amazon Bedrock (in progress)
  - Cut manual claim-entry time from ~1 day/surgery to under 5 minutes; current accuracy 85% and improving
- **Teacher** (Feb 2023 - Jul 2023) - **Aarham Academy**
  - Taught math and science to students through 10th grade for 6 months
- **Core BOD (volunteer leadership)** (Mar 2021 - Jul 2023) - **Rotaract Club of Indus University**
  - Led CSR initiatives, coordinating with external sponsors, concurrent with undergraduate studies
- **Python Intern** (Jun 2021 - Aug 2021) - **InfoLabz**
- **QA Tester** (Aug 2020 - Dec 2020) - **Sunflower Labs** (during break between undergraduate diploma and Bachelor's)

### Independent Projects
- **Image Color-Pattern Clustering Tool** (Apr 2024 - Sep 2024, freelance): Python + OpenCV clustering tool to identify user-defined color patterns in images. Reached 70% completion before the client discontinued the engagement prior to deployment.

### Technical Skills
- **Primary:** Python (advanced) - LangChain, LangGraph, Hugging Face Transformers, Scikit-learn, Keras, TensorFlow, PyTorch, OpenCV
- **Secondary:** JavaScript, SQL, FastAPI; LLM tool/function-calling (in LangGraph)
- **LLM providers/APIs:** OpenAI, Amazon Bedrock (Amazon Nova v1 Pro), Google AI Studio (multi-provider, comfortable switching models)
- **Domain:** Adaptable across domains; growing edge in healthcare (IONM data / insurance claims automation)
- **Software:** VS Code, IntelliJ, AWS (incl. Amazon Bedrock), Docker, Git, DynamoDB, PostgreSQL

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
