# Legal Contract Risk Analyzer

> A compliance-gated skill that reviews employment, lease, partnership, SaaS, and other contracts **clause-by-clause**, surfaces risky / one-sided / hidden-trap clauses in **plain language**, and produces a prioritized **negotiation roadmap** for non-lawyers.
>
> **Educational only - NOT legal advice.** The skill never issues enforceability rulings (that is the unauthorized practice of law). It presents considerations and recommends a licensed attorney for binding matters.

[![Status](https://img.shields.io/badge/status-production--ready-brightgreen)]()
[![Phases](https://img.shields.io/badge/phases-0--5-100%25-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)]()
[![Safety](https://img.shields.io/badge/safety-UPL--gated-critical)]()

---

## Table of Contents

1. [Overview](#overview)
2. [Why this exists](#why-this-exists)
3. [Key features](#key-features)
4. [How it works (gated pipeline)](#how-it-works-gated-pipeline)
5. [Repository structure](#repository-structure)
6. [Quick start](#quick-start)
7. [Knowledge pipeline (`knowledge_updater.py`)](#knowledge-pipeline-knowledge_updaterpy)
8. [Clause category library](#clause-category-library)
9. [Risk rating & scoring](#risk-rating--scoring)
10. [Compliance / safety posture](compliance--safety-posture)
11. [Testing & validation](#testing--validation)
12. [Cross-skill wiring](#cross-skill-wiring)
13. [Configuration](#configuration)
14. [Production run notes](#production-run-notes)
15. [Contributing](#contributing)
16. [License](#license)
17. [Disclaimer](#disclaimer)

---

## Overview

**Legal Contract Risk Analyzer** is an open-source, compliance-gated analysis harness grounded in world-renowned contract-review methods:

- **Risk-allocation analysis** (Restatement-style: who bears liability, indemnity, loss)
- **ABA contract-drafting principles** (clarity, defined terms, completeness, consistency)
- **Unconscionability factors** (procedural + substantive)
- **Restrictive-covenant reasonableness** (duration, geography, scope, legitimate interest, hardship, public interest)
- **Consumer-protection norms** (FTC/CFPB, tenant protections)
- **Plain-language principle** (translate legalese without losing meaning)

It walks a contract clause-by-clause, rates each clause **role-relatively** (employee vs employer, tenant vs landlord, partner vs partner), explains the issue plainly, lists missing protections, computes an overall risk band, and emits a concrete negotiation/redline roadmap. A mandatory **compliance gate with veto power** enforces not-legal-advice framing, jurisdiction caveats, attorney referral scaled to stakes, and prevents unauthorized practice of law (UPL).

A weekly knowledge pipeline (`tools/knowledge_updater.py`) crawls public legal sources (SSRN, ABA, Cornell LII) and appends deduplicated, jurisdiction-tagged findings to the living knowledge base.

---

## Why this exists

Non-lawyers sign contracts without understanding risk allocation, termination terms, liability, hidden fees, auto-renewal traps, and unfair clauses. This skill gives them a structured, plain-language risk map and a referral pathway to licensed counsel - not a verdict.

| User | Question the skill answers |
|------|----------------------------|
| Employee | "Is this non-compete fair / restrictive?" |
| Tenant | "What is risky in this lease?" |
| Founder | "Review this partnership agreement" |
| Customer | "Are these SaaS terms one-sided?" |

---

## Key features

- **Clause-by-clause risk screen** with role-relative ratings (Critical / High / Medium / Low / Info).
- **12-category clause library** (C1 Termination/notice ... C12 Governing law) with red flags and review questions.
- **Weighted overall risk band** (5 dimensions, auditable per-dimension scores).
- **Missing-protection scan** (protections absent for the user role, not just present clauses).
- **Prioritized negotiation roadmap** with concrete redlines, rationale, and must-fix vs nice-to-have vs walk-away.
- **Compliance gate with veto** - no output emitted until `verdict == Pass`.
- **UPL guard** - softens any definitive ruling; never asserts "enforceable/unenforceable/you will win".
- **Citation discipline** - only session-traced sources; no fabricated citations.
- **Jurisdiction + stakes capture** with foreign-law and offline/degraded limits flagged.
- **Living knowledge base** auto-grown by a multi-backend crawler with dedupe and a UPL safety filter.
- **Cross-skill reuse** - exports `sub-compliance-check` and `sub-risk-screener` via a stable interface contract to sibling skills.

---

## How it works (gated pipeline)

```
1. requirements   -> sub-requirements-gatherer   [GATE: jurisdiction + role set or BLOCK]
2. risk screen    -> sub-risk-screener           [GATE: every clause rated + reason]
3. research       -> main harness (WebSearch)     [GATE: cited, jurisdiction-tagged]
4. compliance     -> sub-compliance-check        [GATE/VETO: Pass before output]
5. roadmap        -> sub-improvement-roadmap      [GATE: each item rationale]
6. synthesize     -> main harness renders report   [GATE: re-pass if roadmap edited]
```

### Output format

```
# Contract Risk Report - <type> (<jurisdiction>)
## 0. Disclaimer & Scope
## 1. Context
## 2. Risk Summary (overall band, top clauses, walk-away triggers)
## 3. Clause-by-Clause Risk Table
## 4. Missing Protections
## 5. Negotiation Roadmap
## 6. Attorney Referral (scaled to stakes)
## 7. Sources & Currency (jurisdiction-tagged, offline flag)
```

---

## Repository structure

```
legal-contract-risk-analyzer/
|-- CLAUDE.md                            # skill manifest + status
|-- CROSS-SKILL-WIRING.md                # reusable sub-skill interface contract
|-- PROJECT-detail.md                    # full design spec
|-- PROJECT-DEVELOPMENT-PHASE-TRACKING.md# phase tracker (100% done)
|-- README.md                            # this file
|-- SECOND-KNOWLEDGE-BRAIN.md            # living knowledge base (12 categories + rubric)
|-- skills/
|   |-- main.md                          # main harness (gated pipeline)
|   |-- sub-requirements-gatherer.md     # context capture + BLOCK gate
|   |-- sub-risk-screener.md             # clause risk rating (role-relative)
|   |-- sub-compliance-check.md          # UPL / disclaimer / referral veto gate
|   `-- sub-improvement-roadmap.md       # negotiation/redline roadmap
|-- tests/
|   `-- test-scenarios.md                # 8 conformance scenarios + pipeline self-test
`-- tools/
    |-- knowledge_updater.py             # multi-backend crawler
    |-- knowledge_updater.ini            # source list + options
    |-- fixtures.json                    # offline fixture data
    `-- requirements.txt                  # optional runtime dependencies
```

---

## Quick start

### Requirements

- Python 3.9+
- (Optional) `requests` + `beautifulsoup4` for live HTTP crawling. Without them the tool degrades gracefully to built-in fixtures / `crawl4ai` if installed.

### Install (optional deps)

```bash
pip install -r tools/requirements.txt
```

### Run the knowledge pipeline

```bash
# Internal smoke test (hashing, dedupe, UPL filter, jurisdiction tagging)
python tools/knowledge_updater.py --self-test

# Offline dry-run using fixtures (no network, no file write)
python tools/knowledge_updater.py --offline --dry-run --limit 5

# Live crawl, preview only (no write to brain)
python tools/knowledge_updater.py --dry-run

# Live crawl + append deduped entries to SECOND-KNOWLEDGE-BRAIN.md
python tools/knowledge_updater.py

# Limit + filter sources + config file
python tools/knowledge_updater.py --limit 20 --sources "SSRN,Cornell LII" \
    --config tools/knowledge_updater.ini
```

### Run the analysis skill

Invoke the skill in any Claude/agent runtime that supports the skill format. Provide the contract text; the harness will:

1. Gather jurisdiction + party role (blocks if unknown).
2. Rate every clause role-relatively.
3. Verify current standards (online) or use the brain (offline, flagged).
4. Run the compliance gate (veto until Pass).
5. Emit the roadmap and report.

---

## Knowledge pipeline (`knowledge_updater.py`)

A production-grade crawler that keeps the knowledge base current.

| Capability | Detail |
|------------|--------|
| Backends | `requests`+`BeautifulSoup4` (preferred) -> `crawl4ai` (optional) -> built-in fixtures (offline) |
| Dedupe | 12-char SHA-1 of `url + title`; never appends a duplicate |
| Jurisdiction tagging | auto-detected from title text (US, EU, UK, CA, NY, TX, ...) or `GEN` |
| UPL safety filter | rejects any candidate asserting a definitive enforceability ruling |
| Scoring | keyword relevance + recency bonus; top-N appended |
| Rate limiting | randomized delay between fetches; retry + timeout |
| Config | `tools/knowledge_updater.ini` (sources, limit, delay) overridable by CLI |
| CLI | `--dry-run`, `--offline`, `--limit`, `--sources`, `--config`, `--self-test`, `-v` |
| Schedule | weekly cron |
| Logging | configurable verbosity |

Append format written to `SECOND-KNOWLEDGE-BRAIN.md`:

```
- [DATE] [Jurisdiction] Title - Source - finding - URL <!--h:hash-->
```

---

## Clause category library

The knowledge base defines 12 clause categories. Each carries what/why/risk-vectors/red-flags/review-questions.

| Code | Category | Typical red flags |
|------|----------|-------------------|
| C1 | Termination & notice asymmetry | indefinite lock-in, no cure period, immediate termination for trivial breach |
| C2 | Liability, indemnity & warranty | uncapped unilateral indemnity, asymmetric caps, broad warranty disclaimers |
| C3 | Restrictive covenants | multi-year nationwide non-compete, no sunset, penal liquidated damages |
| C4 | Fees, payment & pricing traps | uncapped annual increases, non-refundable upfront, one-sided attorneys fees |
| C5 | Auto-renewal & term traps | buried short cancellation window, renewal at higher rate |
| C6 | Unilateral amendment | material changes without consent, "deemed acceptance" by use |
| C7 | Dispute resolution | forced individual arbitration + class waiver, distant forum, short limitations |
| C8 | Intellectual property & data | assignment of future unrelated IP, perpetual data license |
| C9 | Liquidated damages & remedies | LD far exceeding plausible harm, sole-remedy wipe-out |
| C10 | Confidentiality scope & survival | perpetual confidentiality, no whistleblower carve-out |
| C11 | Boilerplate with teeth | one-sided assignment, self-caused force majeure, defeating severability |
| C12 | Governing law & jurisdiction | distant forum, weaker-protection law |

---

## Risk rating & scoring

### Per-clause scale (role-relative)

| Rating | Meaning |
|--------|---------|
| Critical | Materially harmful; significant loss/lock-in; or widely disfavored pattern (presented as a consideration, not a ruling) |
| High | Significantly one-sided; meaningful adverse impact; negotiate before signing |
| Medium | Some imbalance/ambiguity; worth clarifying |
| Low | Minor concern; standard but notable |
| Info | Neutral/standard; informational |

### Overall risk band (weighted)

| Dimension | Weight | Anchor |
|-----------|--------|--------|
| Liability / indemnity balance | 25% | Risk-allocation |
| Termination / exit fairness | 20% | Contract norms |
| Restrictive covenants reasonableness | 20% | Non-compete factors |
| Hidden traps (auto-renewal / fees / unilateral change) | 20% | Consumer-protection norms |
| Clarity & completeness | 15% | ABA drafting |

Band mapping (1-5 weighted average): Low (<2.0) - Medium (2.0-3.0) - High (3.1-4.0) - Critical (>4.0).

---

## Compliance / safety posture

The `sub-compliance-check` gate has **veto power**. The harness MUST NOT emit output until `verdict == Pass`.

| Check | What it enforces |
|-------|------------------|
| Disclaimer | prominent "educational, not legal advice; consult an attorney" |
| Jurisdiction caveat | laws vary; verify locally |
| UPL scan | removes/softens any definitive enforceability ruling; replaces with considerations |
| Citation integrity | only session-traced sources; no fabricated citations |
| Referral strength | standard for low/moderate; strong for high/binding/Critical |
| Foreign-law limits | explicit limitation note + local-counsel referral when coverage is partial/none |
| Offline flag | currency-limitation note when offline |
| Roadmap framing | suggestions, not guarantees; Critical/High items carry attorney-review flags |

### UPL softening library (approved replacement phrasing)

| Prohibited | Replaced with |
|------------|---------------|
| "this clause is unenforceable" | "may face enforceability challenges; some jurisdictions limit this pattern" |
| "you will win" | "you may have arguments worth raising; a lawyer can assess your odds on the facts" |
| "is illegal" | "may be restricted or disfavored in some jurisdictions" |
| "this contract is void" | "may contain terms a court could scrutinize; seek advice" |

---

## Testing & validation

`tests/test-scenarios.md` defines 8 conformance scenarios with fixture contracts, context inputs, expected structured outputs, and explicit pass criteria:

1. Overbroad non-compete (employment)
2. Auto-renewal trap (lease)
3. One-sided indemnity (partnership)
4. Foreign-law contract (limits)
5. UPL guard ("is it 100% enforceable?")
6. Offline / degraded mode
7. Low-risk / clean contract (sanity)
8. Unilateral amendment (SaaS/subscription)

Plus the pipeline self-test:

```bash
python tools/knowledge_updater.py --self-test   # prints "self-test OK"
```

Every scenario requires `sub-compliance-check` verdict == Pass before output.

---

## Cross-skill wiring

`CROSS-SKILL-WIRING.md` exports reusable sub-skills via a stable interface contract (version 1.0):

- `sub-compliance-check` - generic legal-safety gate for any skill that could be read as legal advice.
- `sub-risk-screener` - generic role-relative risk rubric.
- `sub-requirements-gatherer`, `sub-improvement-roadmap` - context gate and roadmap builder.

Wired sibling skills (reference-not-fork, veto semantics preserved): 85, 90, 98, 126, 131, 135, 142, 169, 209, 212.

Breaking changes (verdict schema, rating scale, C1-C12 tags) require a major version bump; additions are minor and consumers ignore unknown fields.

---

## Configuration

`tools/knowledge_updater.ini`:

```ini
[sources]
SSRN = https://www.ssrn.com/index.cfm/en/
ABA = https://www.americanbar.org/news/
Cornell LII = https://www.law.cornell.edu/wex

[options]
limit = 25
delay = true
```

CLI flags take precedence over the INI file.

---

## Production run notes

- **Idempotent** - re-running on the same contract + context yields the same ratings given the same brain snapshot.
- **Audit trail** - keep the context object, risk list, compliance verdict, and roadmap as the artifact bundle.
- **Currency** - prefer fresh `WebSearch` each run; fall back to the brain only when offline, and flag it.
- **Deterministic dedupe** - SHA-1(url+title) so re-runs never duplicate brain entries.

---

## Contributing

Contributions are welcome. Please:

1. Keep the compliance gate mandatory and veto-powered.
2. Never add definitive enforceability rulings or fabricated citations.
3. Append-only UPL pattern set and softening library (do not weaken existing safety).
4. Add/extend clause categories without breaking the C1-C12 interface.
5. Run `python tools/knowledge_updater.py --self-test` before submitting.

---

## License

Released under the MIT License. See `LICENSE` for details.

This is an educational tool. It does not provide legal advice and does not create any attorney-client relationship. Use at your own risk; consult a licensed attorney for binding matters.

---

## Disclaimer

**This software is educational and is NOT legal advice.** It does not constitute the practice of law and creates no attorney-client relationship. It does not assert that any clause is enforceable or unenforceable. Legal outcomes depend on jurisdiction and specific facts. Always consult a qualified, licensed attorney in the relevant jurisdiction before signing or relying on any contract.

The knowledge base and pipeline store only public-source findings and patterns; the UPL safety filter rejects any candidate that asserts a definitive legal conclusion.