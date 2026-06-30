# CLAUDE.md - Legal Contract Risk Analyzer Skill (Idea 56)

**Skill name:** `legal-contract-risk-analyzer`
**Tagline:** Plain-language risk analysis of employment/lease/partnership contracts with a remediation roadmap.
**Status:** Production-ready (Phases 0-5 complete, 100%). Educational; compliance-gated by `sub-compliance-check` with veto power.
**Source idea:** 56 - *Analyze legal contracts (employment, lease, partnership) to surface risky/unfavorable clauses in plain language for non-lawyers, grounded in world-renowned legal-review methods, with improvement recommendations; continuously crawl papers/docs to stay current.*
**Cluster:** `legal-compliance` - **COMPLIANCE-GATED: `sub-compliance-check` runs (and must Pass) before any final output.**

## Problem This Skill Solves
Non-lawyers sign contracts without understanding risk. This skill ingests a contract, identifies risky/one-sided clauses against named review checklists (ABA contract drafting principles, risk-allocation analysis, unconscionability factors, restrictive-covenant reasonableness, consumer-protection norms), explains them plainly, and emits a remediation roadmap. **Educational; not legal advice - jurisdiction-dependent; recommends a licensed attorney for binding matters.**

## Harness Flow (gated pipeline)
```
1. requirements   -> sub-requirements-gatherer   [GATE: jurisdiction + role set or BLOCK]
2. risk screen    -> sub-risk-screener            [GATE: every clause rated + reason]
3. research       -> main (WebSearch/WebFetch)    [GATE: cited, jurisdiction-tagged]
4. compliance     -> sub-compliance-check         [GATE/VETO: Pass before output]
5. roadmap        -> sub-improvement-roadmap      [GATE: each item rationale]
6. synthesize     -> main renders report          [GATE: re-pass if roadmap edited]
```

## Sub-skills
`sub-requirements-gatherer.md` | `sub-risk-screener.md` | `sub-compliance-check.md` | `sub-improvement-roadmap.md`

## Tools Required
WebSearch, WebFetch, Read, Write, Bash.

## Knowledge Sources
SSRN legal scholarship, ABA resources, government statute portals, Cornell LII, jurisdiction-specific labor/tenancy law summaries, FTC/CFPB trends.

## Supporting Python Tools
- `tools/knowledge_updater.py` - multi-backend crawler (requests+BS4 / crawl4ai / fixtures), dedupe by SHA-1, UPL safety filter, jurisdiction tagging, INI config, `--self-test`, `--dry-run`, `--offline`.
- `tools/knowledge_updater.ini` - source list + options config.
- `tools/fixtures.json` - offline fixture data.
- `tools/requirements.txt` - optional runtime dependencies.

## Repository Layout
```
legal-contract-risk-analyzer/
  CLAUDE.md
  CROSS-SKILL-WIRING.md          # sub-skill reuse interface for sibling skills
  PROJECT-detail.md
  PROJECT-DEVELOPMENT-PHASE-TRACKING.md
  SECOND-KNOWLEDGE-BRAIN.md      # 12 clause categories, rubric, jurisdiction notes
  skills/
    main.md
    sub-compliance-check.md
    sub-improvement-roadmap.md
    sub-requirements-gatherer.md
    sub-risk-screener.md
  tests/
    test-scenarios.md            # 8 conformance scenarios + pipeline test
  tools/
    knowledge_updater.py
    knowledge_updater.ini
    fixtures.json
    requirements.txt
```

## Active Development Tasks
- [x] Phase 0: research & architecture (frameworks + 12 clause categories + rubric).
- [x] Phase 1: 3 core sub-skills (production-grade).
- [x] Phase 2: main harness + compliance gate (veto).
- [x] Phase 3: knowledge pipeline (production-grade crawler).
- [x] Phase 4: 8 test scenarios + pipeline self-test.
- [x] Phase 5: cross-skill wiring + reuse contract.
- [ ] Expand jurisdiction clause libraries over time (ongoing, via the pipeline).

## Reference Docs
PROJECT-detail.md | PROJECT-DEVELOPMENT-PHASE-TRACKING.md | SECOND-KNOWLEDGE-BRAIN.md | CROSS-SKILL-WIRING.md

## Safety Posture
- No definitive enforceability/outcome rulings (UPL guard).
- No fabricated citations; only session-traced sources.
- Jurisdiction always captured; foreign-law/offline limitations flagged.
- Attorney referral scaled to stakes (strong for binding/high/Critical).