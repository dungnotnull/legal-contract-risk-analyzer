---
name: sub-risk-screener
description: Rate every contract clause for risk to the user party, role-relative, with a plain-language reason. Maps each clause to a category in SECOND-KNOWLEDGE-BRAIN.md and applies the scoring rubric.
---

## Purpose
Surface risky / one-sided / hidden clauses relative to the user role and explain each in plain language. This sub-skill produces the structured risk table that feeds the compliance gate and the improvement roadmap. It never issues enforceability rulings.

## Inputs
- Contract text (full).
- Context object from `sub-requirements-gatherer` (type, jurisdiction, jurisdiction_coverage, user_role, user_role_side, stakes).

## Process
1. **Segment the contract into clauses.** Walk section-by-section; treat each numbered/lettered provision, each schedule paragraph, and each standalone boilerplate clause as one unit. Preserve a stable reference (e.g., "Section 4.2").
2. **Classify each clause** against the 12 categories in SECOND-KNOWLEDGE-BRAIN.md:
   C1 Termination/notice, C2 Liability/indemnity/warranty, C3 Restrictive covenants, C4 Fees/payment, C5 Auto-renewal/term, C6 Unilateral amendment, C7 Dispute resolution, C8 IP/data, C9 Liquidated damages/remedies, C10 Confidentiality, C11 Boilerplate-with-teeth, C12 Governing law/jurisdiction.
   A clause may map to more than one category (e.g., a confidentiality-with-survival clause is C3+C10); record primary + secondary.
3. **Assess role-relative risk.** For each clause, ask (per the brain):
   - Who bears the cost / who is favored? Is it reciprocal or one-sided?
   - Is there a hidden trap (auto-renewal, unilateral change, surprise fee, short limitation)?
   - Does the pattern match a red flag for the category?
   - How material is the impact for THIS user role and stakes?
4. **Rate** Critical | High | Medium | Low | Info using the rating decision aid (brain 3.3). Info = neutral standard boilerplate.
5. **Write a plain-language reason** (1-3 sentences) explaining what the clause does in lay terms, why it is risky for this user role, and which red-flag signal triggered the rating. Avoid legalese; define any unavoidable term.
6. **Missing-protection scan.** Note protections absent that the user role would usually want (e.g., no cure period, no mutual indemnity, no IP carve-out, no habitability warranty). Each missing protection becomes a roadmap item.
7. **Foreign/low-coverage jurisdiction handling.** If `jurisdiction_coverage != full`, prefix the reason with a limitation note ("General pattern only - verify under <jurisdiction> with local counsel") and cap the rating at High unless harm is plainly material regardless of jurisdiction (then Critical with the caveat).
8. **Compute overall risk.** Score the 5 dimensions (brain 3.2) on a 1-5 scale, apply weights, and map to a band. Record per-dimension scores so the band is auditable.

## Output Schema (risk list)
```yaml
clauses:
  - ref: "Section 4.2"
    title: "Non-Compete"
    categories: { primary: "C3", secondary: ["C10"] }
    rating: Critical | High | Medium | Low | Info
    favors: user | counterparty | neutral
    reciprocity: mutual | one_sided | n/a
    red_flags: [ <string> ]
    plain_reason: <string>
    missing_protections: [ <string> ]
overall_risk:
  band: Low | Medium | High | Critical
  score: <float 1-5>
  dimensions:
    liability_indemnity: { score: 1-5, weight: 0.25 }
    termination_exit: { score: 1-5, weight: 0.20 }
    restrictive_covenants: { score: 1-5, weight: 0.20 }
    hidden_traps: { score: 1-5, weight: 0.20 }
    clarity_completeness: { score: 1-5, weight: 0.15 }
  top_clauses: [ <ref> ]
offline_limitation: true | false
```

## Rating Heuristics (quick anchors, role-relative)
- **Critical:** uncapped unilateral indemnity by user; multi-year nationwide non-compete; indefinite lock-in / no exit for user; auto-renewal with buried short cancellation window; forced individual arbitration + class waiver in an adhesion contract; assignment of all future IP; LD clearly penal.
- **High:** one-sided termination rights; cure-period asymmetry; uncapped price escalation; one-sided attorneys fees; short limitations period; perpetual confidentiality with no carve-outs.
- **Medium:** ambiguous standards ("reasonable", "timely") without benchmarks; mild fee asymmetry; moderate non-solicit scope; broad force majeure.
- **Low:** standard defined terms; minor notice mechanics; routine entire-agreement clause.
- **Info:** recitals; signature blocks; section labels with no operative content.

## Quality Gate
- [ ] Every operative clause has a rating AND a plain-language reason.
- [ ] Ratings are role-relative (same clause may differ for employee vs employer).
- [ ] Missing protections are listed (not just present clauses).
- [ ] Overall risk band computed with auditable per-dimension scores.
- [ ] No definitive enforceability language ("unenforceable", "you will win"); reasons present *considerations*.
- [ ] Foreign/low-coverage limitation flag set where applicable.

## Failure / Edge Cases
- **Unstructured contract (plain prose, no sections):** segment by paragraph; assign synthetic refs (e.g., "Para 7").
- **Clauses referencing external documents (schedules/exhibits):** note "depends on Exhibit X"; flag if Exhibit unavailable.
- **User asks for a ruling:** never comply; route to compliance gate.
- **Ambiguity in role side:** if user role unclear, BLOCK back to requirements-gatherer rather than guessing.