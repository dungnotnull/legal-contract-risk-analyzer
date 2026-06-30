# CROSS-SKILL-WIRING.md - Legal Contract Risk Analyzer (Idea 56)

Documents how the reusable sub-skills from this skill are shared with the
listed sibling skills, so they can adopt the same compliance gate and
risk-screening primitives instead of reimplementing them. This is a *contract*
specification: consumer skills depend only on the documented interface, not on
internal implementation details.

---

## 1. Reusable Sub-Skills Exported

| Sub-skill | File | Purpose | Reuse-safe? |
|-----------|------|---------|-------------|
| `sub-compliance-check` | `skills/sub-compliance-check.md` | UPL / disclaimer / jurisdiction / referral gate with veto power | Yes - generic legal-safety gate for ANY skill that could be read as legal advice |
| `sub-risk-screener` | `skills/sub-risk-screener.md` | Role-relative clause risk rating with plain-language reasons | Yes - generic risk-screening rubric; works on any structured clause set |
| `sub-requirements-gatherer` | `skills/sub-requirements-gatherer.md` | Context capture + BLOCK gate | Yes - generic context gate |
| `sub-improvement-roadmap` | `skills/sub-improvement-roadmap.md` | Prioritized negotiation/redline roadmap | Partial - phrasing is contract-oriented; consumer may override vocabulary |

The most widely reusable are `sub-compliance-check` (legal-safety gate) and
`sub-risk-screener` (role-relative risk rubric).

---

## 2. Stable Interface Contracts (what consumers depend on)

### 2.1 sub-compliance-check
- **Input:** draft report text + context `{jurisdiction, jurisdiction_coverage, stakes, user_role}` + optional risk list / roadmap.
- **Output:** `compliance.verdict` in {Pass, Needs-fix} + `edits_required[]` (location, issue, fix) + `referral_strength` in {standard, strong}.
- **Veto semantics:** caller MUST NOT emit output while verdict == Needs-fix; apply edits and re-run.
- **Standalone:** no dependency on contract-specific clause library; uses UPL pattern set + disclaimer/caveat/referral checks. Safe to import verbatim.

### 2.2 sub-risk-screener
- **Input:** clause set + context.
- **Output:** risk list `{clauses[].{ref, title, categories, rating, favors, reciprocity, red_flags, plain_reason, missing_protections}}` + `overall_risk.{band, score, dimensions}`.
- **Reusable rubric:** the rating scale (Critical..Info), role-relative adjustment, and the 12 category tags (C1..C12) are domain-general enough for risk screening; consumer skills may extend categories with their own clause catalog.

### 2.3 sub-requirements-gatherer / sub-improvement-roadmap
- Context gate and roadmap builder; consumers reuse as-is or override vocabulary.

---

## 3. Consumer Skills (wiring targets)

The following sibling skills are wired to reuse the exported sub-skills (by
reference, with the shared copy kept canonical in this repo):

| Skill ID | Domain | Reused sub-skill(s) | Wiring mode |
|----------|--------|----------------------|-------------|
| 85 | Tenant rights / lease review | sub-compliance-check, sub-risk-screener | Import gate + rubric; lease clause lib local |
| 90 | Employment terms explainer | sub-compliance-check, sub-risk-screener | Import gate + rubric |
| 98 | Small-business contract review | sub-compliance-check, sub-risk-screener, sub-improvement-roadmap | Full import |
| 126 | NDA / confidentiality review | sub-compliance-check, sub-risk-screener | Import gate + C3/C10 focus |
| 131 | SaaS / subscription terms review | sub-compliance-check, sub-risk-screener | Import gate + C4/C5/C6 focus |
| 135 | Partnership / founder agreement review | sub-compliance-check, sub-risk-screener, sub-improvement-roadmap | Full import |
| 142 | Vendor / procurement contract review | sub-compliance-check, sub-risk-screener | Import gate + C2/C4 focus |
| 169 | Consumer contract fairness | sub-compliance-check, sub-risk-screener | Import gate + consumer-protection overlay |
| 209 | Dispute-resolution clause analyzer | sub-compliance-check, sub-risk-screener | Import gate + C7 focus |
| 212 | IP assignment / work-for-hire review | sub-compliance-check, sub-risk-screener | Import gate + C8 focus |

---

## 4. Wiring Protocol (how a consumer adopts)

1. **Reference, do not fork:** consumer skills link to the canonical sub-skill
   file path in this repo (e.g., `legal-contract-risk-analyzer/skills/sub-compliance-check.md`)
   and invoke it; they do not maintain a divergent copy.
2. **Adhere to the interface:** consumer must respect veto semantics
   (never emit while Needs-fix) and the output schema.
3. **Extend, do not break:** a consumer may add domain-specific clause
   categories (e.g., skill 209 adds C7 sub-types) but MUST keep the shared
   rating scale and compliance checks intact.
4. **Shared SECOND-KNOWLEDGE-BRAIN.md:** the brain is shared read-only by
   consumers; `tools/knowledge_updater.py` is the only writer and tags entries
   so consumer skills can filter by jurisdiction/category.

---

## 5. Compatibility & Versioning

- Interface version: 1.0. Changes to `compliance.verdict`, the rating scale, or
  the C1..C12 category tags are breaking and require a major bump.
- Non-breaking additions (new red-flag patterns, new optional output fields)
  are minor bumps; consumers MUST ignore unknown fields.
- The UPL pattern set and softening library are append-only.

---

## 6. Verification

- Consumer skill must pass its own compliance gate using the shared
  `sub-compliance-check` before any output (same veto semantics).
- The 8 scenarios in `tests/test-scenarios.md` serve as the conformance suite
  for the shared gate and rubric; consumers reuse scenarios 4 (foreign-law
  limits) and 5 (UPL guard) as their minimum acceptance tests.