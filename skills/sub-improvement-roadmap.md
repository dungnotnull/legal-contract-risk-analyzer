---
name: sub-improvement-roadmap
description: Turn risk-rated clauses into a prioritized, plain-language negotiation/redline roadmap with rationale, must-fix vs nice-to-have priority, and an attorney-review recommendation for high-stakes items. Educational suggestions only - never legal guarantees.
---

## Purpose
Give the user an actionable, prioritized plan to negotiate, redline, or walk away. Each item must reference the clause, explain the issue plainly, propose a fairer alternative, and justify it. This is the "so what do I do" layer after the risk screen.

## Inputs
- Risk list from `sub-risk-screener` (clauses with ratings, categories, plain reasons, missing protections).
- Context from `sub-requirements-gatherer` (goals, constraints, stakes, user role).
- Compliance constraints from `sub-compliance-check` (disclaimer required, no UPL, referral strength).

## Process
1. **Sort by priority.** Critical first, then High, then Medium. Group related clauses (e.g., all auto-renewal + termination items together) for coherent negotiation.
2. **For each risky clause, build a roadmap item** with these fields:
   - clause_ref, clause_title, rating, category.
   - issue_plain: plain-language restatement of the problem (max 2 sentences).
   - why_it_matters: the user-role consequence ("if this stays, you could ...").
   - suggested_redline: concrete alternative language or direction (e.g., "cap non-compete to 12 months and to the region you actually work in", "make indemnity mutual with a shared cap", "add a 30-day cure period before termination for any breach").
   - rationale: why the suggestion is fairer (anchor to a brain framework: risk-allocation, drafting clarity, restrictive-covenant reasonableness, consumer-protection).
   - priority: must_fix_before_signing | nice_to_have | walk_away_trigger.
   - negotiation_tactic: a short tip (e.g., "frame as industry standard", "offer a mutual version", "ask for a cure period in exchange").
3. **Walk-away triggers.** If one or more Critical items cannot be modified and stakes are binding/high, mark the contract "walk_away_trigger" and put a strong attorney-referral at the top.
4. **Attorney-review recommendation.** For every Critical and High item, append "Review with a licensed attorney before signing." Scale referral strength with stakes.
5. **Address missing protections.** Convert each missing protection from the risk screen into a roadmap item to *add* (not just redline). E.g., "No cure period -> add a 30-day cure right for material breaches."
6. **Goals alignment.** If the user goal is `sign_as_is`, emphasize must-fix vs nice-to-have so they know what they accept; if `negotiate`, lead with the must-fix redlines; if `walk_away`, surface walk-away triggers first; if `sanity_check`, keep it concise with the top 3-5 items.
7. **Frame as suggestions.** Every item is a suggestion ("consider", "you may want to ask for"), never a legal guarantee or definitive outcome.

## Output Schema (roadmap)
```yaml
roadmap:
  - clause_ref: "Section 4.2"
    clause_title: "Non-Compete"
    rating: Critical
    category: C3
    issue_plain: <string>
    why_it_matters: <string>
    suggested_redline: <string>
    rationale: <string; framework anchor>
    priority: must_fix_before_signing | nice_to_have | walk_away_trigger
    negotiation_tactic: <string>
    attorney_review: true | false
walk_away: true | false
referral_strength: standard | strong
summary:
  must_fix_count: <int>
  nice_to_have_count: <int>
  top_3: [ <clause_ref> ]
```

## Priority Decision Aid
- **must_fix_before_signing:** Critical or High items that materially shift risk to the user with no reciprocity, OR any binding stakes + Critical item.
- **nice_to_have:** Medium/Low clarifications, mild symmetry fixes.
- **walk_away_trigger:** Critical item that the counterparty will not change AND stakes are binding/high (e.g., uncapped unilateral indemnity + no exit).

## Quality Gate
- [ ] Critical/High clauses addressed first with a concrete suggested change.
- [ ] Each item has a rationale anchored to a brain framework.
- [ ] Each item references the clause (clause_ref + title).
- [ ] Walk-away triggers surfaced when applicable; referral strength scales with stakes.
- [ ] Missing protections converted to "add" items.
- [ ] All items framed as suggestions, not guarantees; no UPL language.
- [ ] Roadmap aligned to the user goal (sign/negotiate/walk/sanity).

## Failure / Edge Cases
- **No risky clauses (all Low/Info):** emit a short "low-risk" summary with 0 must-fix and a standard "still have an attorney review high-stakes" note.
- **User cannot negotiate (take-it-or-leave-it, adhesion):** state that explicitly; shift advice to "what you are accepting" + walk-away option + attorney referral.
- **Foreign/low-coverage jurisdiction:** prefix suggested redlines with "general best practice - confirm local law" and scale referral to strong.