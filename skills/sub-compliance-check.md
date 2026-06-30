---
name: sub-compliance-check
description: Mandatory legal-safety gate with VETO power. Enforces not-legal-advice framing, jurisdiction caveat, attorney referral, and prevents unauthorized practice of law (UPL). Runs before final synthesis; if it returns Needs-fix the harness must apply edits and re-run.
---

## Purpose
Keep the skill responsible and non-UPL. The skill is *educational*; it must never issue definitive legal conclusions ("this clause is enforceable/unenforceable", "you will win/lose"), never fabricate citations, and always frame output with disclaimers, jurisdiction caveats, and attorney referral scaled to stakes. This gate has veto power: a draft that fails is returned for editing before output.

## Inputs
- Draft report (all sections from main harness): disclaimer, summary, clause table, roadmap, sources.
- Context (jurisdiction, jurisdiction_coverage, stakes, user_role).
- Risk list and roadmap (to scan for UPL phrasing).

## Process (checks run in order; any failure -> Needs-fix with specific edits)
1. **Disclaimer present & prominent.** Confirm the report contains an explicit, near-top disclaimer stating this is educational, not legal advice, and recommending a licensed attorney for binding matters.
2. **Jurisdiction caveat present.** Confirm a caveat that laws vary by jurisdiction and that findings are general patterns to verify locally. If jurisdiction_coverage != full, confirm an explicit limitation note is present and prefixed to affected clauses.
3. **UPL scan.** Scan the draft for prohibited definitive language and either remove it or soften to a *consideration*. Prohibited patterns (regex, case-insensitive):
   - "this clause is (un)?enforceable"
   - "you will (win|lose|prevail)"
   - "this is (definitely|clearly|100%) (legal|illegal|binding)"
   - "the contract is (void|valid)"
   - any assertion of a definitive legal outcome.
   Replace with: "This clause raises considerations about enforceability - patterns X suggest reviewing with counsel; outcome depends on jurisdiction and facts."
4. **Citation integrity.** Confirm every statute/case citation in the report is either (a) from a verified WebSearch/WebFetch result in this run, or (b) marked "general pattern, verify". Flag and strip any citation that cannot be traced to a source captured in this session. Never invent citations.
5. **Referral strength matches stakes.**
   - stakes = binding or Critical items present -> strong referral ("Strongly recommended: have a licensed attorney review before signing").
   - stakes = high -> standard-strong referral.
   - stakes = moderate/low -> standard referral ("Consult a licensed attorney for binding matters").
6. **Foreign-law limits.** If jurisdiction_coverage = none/partial, confirm the limitation note and local-counsel referral are present and that no jurisdiction-specific definitive claim is made.
7. **Offline/degraded flag.** If offline_mode, confirm a currency limitation note is present ("Legal-currency not verified this run; confirm current law via counsel/WebSearch").
8. **Roadmap framing.** Confirm roadmap items are framed as suggestions, not guarantees, and that must-fix items carry attorney-review flags where Critical/High.

## Output Schema (verdict)
```yaml
compliance:
  verdict: Pass | Needs-fix
  edits_required:
    - location: <section/clause ref>
      issue: <string>
      fix: <string>
  checks:
    disclaimer: Pass | Fail
    jurisdiction_caveat: Pass | Fail
    upl_scan: Pass | Fail
    citation_integrity: Pass | Fail
    referral_strength: Pass | Fail
    foreign_law_limits: Pass | Fail
    offline_flag: Pass | Fail | N/A
    roadmap_framing: Pass | Fail
  referral_strength: standard | strong
  notes: <string>
```

## UPL Softening Library (approved replacement phrasing)
- Definitive ruling -> "raises considerations; outcome depends on jurisdiction and facts; review with counsel."
- "unenforceable" -> "may face enforceability challenges; some jurisdictions limit this pattern."
- "you will win" -> "you may have arguments worth raising; a lawyer can assess your odds on the facts."
- "is illegal" -> "may be restricted or disfavored in some jurisdictions."
- "this contract is void" -> "this contract may contain terms a court could scrutinize; seek advice."

## Veto Behavior
- If `verdict == Needs-fix`, the harness MUST apply every listed edit and re-run the gate. The final report must not be emitted until `verdict == Pass`.
- The gate never *creates* new risk findings; it only edits framing/citations/referral.

## Quality Gate
- [ ] Disclaimer + jurisdiction caveat + attorney referral present and match stakes.
- [ ] Zero definitive enforceability / outcome rulings remain (UPL scan Pass).
- [ ] All citations traceable or marked "verify"; none fabricated.
- [ ] Foreign-law and offline limitations flagged where applicable.
- [ ] Roadmap framed as suggestions; Critical/High items carry attorney-review flags.

## Failure / Edge Cases
- **User explicitly asks for a ruling ("is it 100% enforceable?"):** do NOT answer the ruling; the gate must ensure the response gives considerations + referral instead. If the draft contains a ruling, Needs-fix.
- **Draft has a real citation from a prior session:** mark "verify current" rather than strip; prefer live re-verification.
- **Adhesion/no-negotiation contract:** ensure the report says the user is accepting terms as-is and escalates referral strength.