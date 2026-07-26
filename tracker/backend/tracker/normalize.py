"""Fuzzy company/role matching used to dedupe scraped leads against applications.

Perfect dedup is impossible programmatically: the CSV and seen_jobs.json record
the same job under slightly different names (``CNN`` vs ``CNN (NYC)``,
``NYU Langone`` vs ``NYU Langone Health``, ``Backend Engineer`` vs
``Software Engineer, Backend``). ``/scrape`` deduped these semantically. Here we
use a conservative rule that never *hides* a genuinely-different lead:

- **company match**: normalized company token-sets are subset-equal either way
  (``{nyu, langone} ⊆ {nyu, langone, health}``), so trailing descriptors match.
- **role match (exact)**: normalized role token-sets are equal. Strict on purpose
  so two distinct roles at one company (e.g. Notion "Early Career" vs
  "Early Career (AI)") are never collapsed.

A lead with an exact company+role match is hidden (already applied). A lead that
matches only on company is *shown* but tagged ``possible_duplicate`` so the UI can
surface a soft "already applied here?" hint; the user resolves the rest with the
per-card dismiss action.
"""

import re

# Legal-suffix / noise tokens dropped from company names before matching.
_COMPANY_NOISE = {
    "inc", "llc", "ltd", "limited", "corp", "corporation", "co", "gmbh",
    "plc", "sa", "ag", "as", "aps", "group", "holding", "holdings",
    "technologies", "solutions", "yc",
}

_PARENS = re.compile(r"\([^)]*\)")
_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def _tokens(s: str) -> list[str]:
    return [t for t in _NON_ALNUM.split((s or "").lower()) if t]


def company_tokens(name: str) -> frozenset[str]:
    """Normalized company tokens: parentheticals and legal/geo noise stripped."""
    stripped = _PARENS.sub(" ", name or "")
    return frozenset(t for t in _tokens(stripped) if t not in _COMPANY_NOISE)


def role_tokens(role: str) -> frozenset[str]:
    """Normalized role tokens. Parentheticals are kept (``(AI)`` is meaningful)."""
    return frozenset(_tokens(role))


def company_matches(a: str, b: str) -> bool:
    ta, tb = company_tokens(a), company_tokens(b)
    if not ta or not tb:
        return False
    return ta <= tb or tb <= ta


def role_matches(a: str, b: str) -> bool:
    ta, tb = role_tokens(a), role_tokens(b)
    return bool(ta) and ta == tb
