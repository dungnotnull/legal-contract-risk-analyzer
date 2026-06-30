# PROJECT-detail.md - Legal Contract Risk Analyzer (Idea 56)

## Executive Summary
A compliance-gated harness that reviews a contract clause-by-clause, surfaces risky/one-sided terms in plain language, and emits a negotiation/remediation roadmap - with mandatory jurisdiction capture and not-legal-advice framing. Production-grade and open-source ready. Educational only; never issues enforceability rulings (UPL guard).

## Problem Statement
People sign employment, lease, and partnership agreements without understanding risk allocation, termination terms, liability, or unfair clauses. This skill provides structured, plain-language risk analysis and a referral pathway to licensed counsel.

## Target Users & Use Cases
- **Employee:** "Is this non-compete fair/restrictive?" -> clause risk + plain explanation + redline.
- **Tenant:** "What's risky in this lease?" -> risky-clause list + negotiation points.
- **Founder:** "Review this partnership agreement" -> control/exit/liability risk map.
- **Customer:** SaaS/vendor terms -> unilateral-amendment and pricing-trap flags.

## Harness Architecture (gated pipeline)
```
/legal-contract-risk-analyzer
  -> sub-requirements-gatherer  (type, jurisdiction, role)        [GATE: jurisdiction + role set or BLOCK]
  -> sub-risk-screener          (clause-by-clause risk)           [GATE: each clause rated + reason]
  -> [main] research            (current legal standards)         [GATE: cited, jurisdiction-tagged]
  -> sub-compliance-check       (disclaimer/UPL gate)             [GATE/VETO: Pass before output]
  -> sub-improvement-roadmap    (negotiation/redline)             [GATE: each item rationale]
  -> [main] synthesize                                            [GATE: re-pass if roadmap edited]
```

## Full Sub-Skill Catalog
| Sub-skill | Purpose | Inputs | Outputs | Gate |
|-----------|---------|--------|---------|------|
| sub-requirements-gatherer | Context | contract, jurisdiction, role, goals, constraints, stakes | context object | Jurisdiction + role set or BLOCK |
| sub-risk-screener | Rate clauses (role-relative) | contract text + context | risk list + overall band | Every clause rated + reason; missing protections listed |
| sub-compliance-check | Legal-safety gate (veto) | draft report + context | verdict + edits + referral strength | Pass before output; no UPL; citations traced |
| sub-improvement-roadmap | Negotiation plan | risk list + context | prioritized roadmap | Each item references clause + has rationale |

## Knowledge Base (SECOND-KNOWLEDGE-BRAIN.md)
- 12 clause categories (C1 Termination/notice ... C12 Governing law/jurisdiction).
- 6 analytical frameworks: risk-allocation, ABA drafting, unconscionability, restrictive-covenant reasonableness, consumer-protection norms, plain-language.
- Risk rating scale (Critical..Info) + 5-dimension weighted scoring (liability 25%, termination 20%, restrictive covenants 20%, hidden traps 20%, clarity 15%).
- Role-relative adjustment (employee/employer/tenant/landlord/partner/other).
- Jurisdiction notes (patterns to investigate, not rulings) + foreign-law/offline limits.

## E2E Execution Flow
1. Gather contract type, governing-law jurisdiction, and which party the user is (block if unknown).
2. Risk screener rates each clause role-relatively and lists missing protections.
3. Research verifies current enforceability standards (jurisdiction-tagged); offline uses brain + flags currency.
4. Compliance check enforces not-legal-advice framing, jurisdiction caveat, attorney referral, and NO UPL-style definitive verdicts; veto until Pass.
5. Roadmap gives plain explanations + negotiation/redline suggestions per risky clause with rationale.
6. Synthesize the final report.

## Error Handling
- Missing jurisdiction/role -> BLOCK and request; never assume.
- Binding/high-stakes or Critical item -> strong attorney referral; surface walk-away triggers.
- Foreign law not covered -> general patterns only; explicit limitation note; strong local-counsel referral.
- Offline/degraded -> use brain, flag currency limitation, compliance gate still runs.
- User demands a ruling -> compliance gate prevents it; respond with considerations + referral.

## Knowledge Pipeline (tools/knowledge_updater.py)
- Multi-backend fetch: requests+BeautifulSoup (preferred), crawl4ai (optional), fixtures (offline).
- Dedupe by 12-char SHA-1(url+title); UPL safety filter rejects definitive rulings; jurisdiction tagging.
- INI config + CLI (`--dry-run`, `--offline`, `--limit`, `--sources`, `--config`, `--self-test`, `-v`).
- Rate limiting + retry + timeout; logs; idempotent. Weekly cron schedule.

## SECOND-KNOWLEDGE-BRAIN Integration
Sources: SSRN, ABA, Cornell LII, government statute portals, FTC/CFPB. Weekly append, jurisdiction-tagged, deduped.

## Quality Gates
- Each clause has a risk rating + plain-language reason; missing protections listed.
- Compliance gate: not-legal-advice disclaimer + jurisdiction caveat + scaled attorney referral; no UPL verdicts; no fabricated citations.
- Roadmap items reference the clause and give rationale; framed as suggestions.
- Foreign-law/offline limitations flagged where applicable.
- Overall risk band computed with auditable per-dimension scores.

## Test Scenarios (tests/test-scenarios.md)
8 conformance scenarios incl. UPL guard (S5), foreign-law limits (S4), offline mode (S6), low-risk sanity (S7), unilateral amendment (S8). Plus pipeline self-test (`python tools/knowledge_updater.py --self-test`).

## Cross-Skill Wiring (CROSS-SKILL-WIRING.md)
Exports `sub-compliance-check` and `sub-risk-screener` (plus the other two sub-skills) via a stable interface contract to sibling skills 85, 90, 98, 126, 131, 135, 142, 169, 209, 212. Reference-not-fork; veto semantics preserved; interface version 1.0.

## Key Design Decisions
1. Compliance gate mandatory with veto power.
2. No definitive enforceability rulings (avoid UPL).
3. Jurisdiction always captured; coverage flag set.
4. Role-relative ratings.
5. Plain-language explanations.
6. Strong referral for binding/high-stakes and Critical items.
7. Citation discipline: session-traced sources only; brain-only patterns marked "verify locally".