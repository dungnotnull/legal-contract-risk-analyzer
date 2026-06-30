# SECOND-KNOWLEDGE-BRAIN.md - Legal Contract Risk Analyzer (Idea 56)

Living knowledge base, grown weekly by `tools/knowledge_updater.py`. All entries are jurisdiction-tagged. **Educational only - NOT legal advice.** No entry here is a definitive ruling; always recommend a licensed attorney for binding matters.

---

## 0. Scope & Disclaimer

This brain supports a plain-language, *educational* contract-risk review for non-lawyers. It catalogs clause categories, risk frameworks, scoring rubrics, and jurisdiction notes to help the analyst *surface and explain* risk - it never asserts that a clause is "enforceable" or "unenforceable" as a legal conclusion. Such conclusions are the unauthorized practice of law (UPL). Where binding/high-stakes, refer to licensed counsel.

Currency: legal standards move; entries are timestamped. Always verify recency via WebSearch and flag offline/degraded mode.

---

## 1. Core Analytical Frameworks

| Framework | Origin | Use here |
|-----------|--------|----------|
| Risk-allocation analysis | Contract theory / Restatement (Second) of Contracts principles | Identify who bears liability, indemnity, loss; measure one-sidedness vs balance. |
| ABA contract-drafting principles | ABA Section of Business Law drafting guides | Evaluate clarity, defined terms, completeness, consistency, organization. |
| Unconscionability factors | Procedural + substantive unconscionability doctrine | Flag oppressive terms + bargaining-power/surprise problems. |
| Restrictive-covenant reasonableness | Non-compete case-law factors (duration, geography, scope, legitimate interest, hardship, public interest) | Assess non-compete / non-solicit / confidentiality overbreadth. |
| Consumer-protection norms | FTC/CFPB guidance, tenant-protection statutes | Detect hidden traps (auto-renewal, surprise fees, unilateral changes). |
| Plain-language principle | Plain Language Action Network / ABA plain-language guidance | Translate legalese to lay terms without losing meaning. |

### 1.1 Risk-allocation lens (apply per clause)
- Who bears the cost if things go wrong? (liability, indemnity, warranty gaps)
- Is the allocation reciprocal (mutual) or unilateral?
- Are caps/exclusions asymmetric between parties?
- Is there a duty to mitigate, cure periods, notice obligations - symmetric or one-sided?

### 1.2 ABA drafting checklist
- Defined terms used consistently; no orphaned definitions.
- No ambiguity ("reasonable", "timely") without benchmarks.
- Complete obligations (who/what/when/how).
- Organized logically; cross-references resolve.
- Boilerplate read for hidden effect (entire-agreement, severability, waiver, assignment).

### 1.3 Unconscionability factors
- Procedural: adhesion/standard form, surprise/hidden terms, fine print, take-it-or-leave-it, no meaningful choice.
- Substantive: oppressive price/terms, harsh remedies, one-sided risk, unfair surprise.

### 1.4 Restrictive-covenant reasonableness factors
1. Legitimate business interest (protectable?)
2. Duration (reasonable?)
3. Geographic scope (reasonable?)
4. Activity/scope restricted (narrowly tailored?)
5. Hardship on the restricted party
6. Public interest impact
7. Consideration given (at hire vs upon termination)

---

## 2. Clause Category Library

Each category lists: what it is, why it matters, role-relative risk vectors, red flags, and review questions. Categories are jurisdiction-general; enforceability varies.

### C1. Termination & notice asymmetry
- **What:** Who can end the contract, for what cause, with how much notice, and what happens on exit.
- **Why:** Asymmetric termination lets one party exit freely while locking the other in.
- **Risk vectors:** at-will vs cause-only termination; short vs long notice; termination-for-convenience only one side; cure-period asymmetry; post-termination obligations (transition, data return).
- **Red flags:** indefinite lock-in for one party; no cure period for the user while other party has one; immediate termination for trivial breach; forfeiture of paid amounts on termination.
- **Review questions:** Can the user exit on reasonable notice? Is there a cure right before termination? What survives termination?

### C2. Liability, indemnity & warranty
- **What:** Who pays for losses, who indemnifies whom, warranty scope and disclaimers, liability caps and exclusions.
- **Why:** Risk allocation core; one-sided indemnity shifts all loss to one party.
- **Risk vectors:** unilateral vs mutual indemnity; cap on liability excluding one party IP/consequential; broad third-party-claim indemnity; warranty disclaimers favoring one side; "hold harmless" scope.
- **Red flags:** uncapped indemnity by user while other party capped; indemnity for the other party own negligence/willful misconduct; warranty disclaimers eroding all user remedies.
- **Review questions:** Is indemnity mutual? Are caps symmetric? Are consequential damages excluded symmetrically? Is there a defense/control obligation for indemnified claims?

### C3. Restrictive covenants (non-compete / non-solicit / confidentiality)
- **What:** Post-contract limits on competing, soliciting, using confidential info.
- **Why:** Can block future work/income; enforceability jurisdiction-dependent and often narrowing (e.g., FTC rule developments, state bans).
- **Risk vectors:** duration (months vs years), geographic breadth, activity scope, garden leave, customer/employee non-solicit, confidentiality survival period, IP/return-of-materials.
- **Red flags:** multi-year nationwide ban; no geographic limit; restriction beyond protectable interest; no sunset; liquidated damages for breach.
- **Review questions:** Is the scope tied to a legitimate interest? Is duration/geography reasonable? Does it survive termination without cause? What hardship if enforced?

### C4. Fees, payment & pricing traps
- **What:** What the user pays, when, and the consequences of non-payment.
- **Why:** Hidden fees, automatic increases, and harsh late/termination charges erode value.
- **Risk vectors:** auto-increase clauses, CPI/uncapped escalation, late fees, default interest, collection costs/attorneys fees one-sided, security deposits, upfront non-refundable fees.
- **Red flags:** uncapped annual price increases; non-refundable large upfront; one-sided attorneys fees clause; acceleration of all payments on any breach.
- **Review questions:** When can price change and by how much? What is refundable? Who pays dispute costs?

### C5. Auto-renewal & term traps (evergreen)
- **What:** How long the contract runs and whether/how it renews.
- **Why:** Evergreen clauses lock users in; missed cancellation windows bind them.
- **Risk vectors:** automatic renewal, cancellation notice window (e.g., 90 days), renewal price terms, initial vs renewal term length.
- **Red flags:** short cancellation window buried in boilerplate; renewal at higher rate; no easy opt-out; indefinite auto-renew.
- **Review questions:** How does the user cancel and by when? Is there a reminder/notice duty? What is the renewal rate?

### C6. Unilateral amendment & change control
- **What:** Who can change terms and how.
- **Why:** Unilateral change clauses let one party rewrite the deal later.
- **Risk vectors:** "we may amend at any time"; change effective on continued use; no notice; material changes without consent.
- **Red flags:** unilateral material changes without consent or notice; "deemed acceptance" by use; retroactive changes.
- **Review questions:** Who can amend? What notice/consent is required? Can the user reject and exit?

### C7. Dispute resolution (arbitration / forum / class waiver)
- **What:** Where and how disputes are resolved.
- **Why:** Mandatory arbitration, remote forums, and class waivers can limit user remedies.
- **Risk vectors:** mandatory individual arbitration, class-action waiver, remote forum-selection, choice-of-law, short limitations periods, cost-shifting, appeal limits.
- **Red flags:** forced individual arbitration + class waiver; distant forum; very short limitations period; loser-pays for user only.
- **Review questions:** Can the user go to court? Is a class action possible? Is the forum accessible? Is the limitations period fair?

### C8. Intellectual property & data
- **What:** Who owns created IP, who licenses background IP, data usage rights.
- **Why:** Over-broad IP assignment or license can strip future value.
- **Risk vectors:** work-for-hire scope, assignment of future inventions, license-back breadth, portfolio/perpetual license, feedback license, data usage for product improvement.
- **Red flags:** assignment of all future IP unrelated to scope; perpetual irrevocable license to user data/content; no carve-out for prior IP.
- **Review questions:** Is IP scope limited to the engagement? Is there a license-back? Are pre-existing rights carved out?

### C9. Liquidated damages & remedies
- **What:** Pre-set damages for breach and remedy limits.
- **Why:** Penalty-like liquidated damages and one-sided remedy limits disadvantage one party.
- **Risk vectors:** LD as penalty (disproportionate to harm), cumulative vs exclusive remedies, limitation of remedies, cure-before-remedy requirements.
- **Red flags:** LD far exceeding plausible harm; sole remedy that wipes out recovery; no LD reciprocity.
- **Review questions:** Does LD approximate actual harm? Are remedies reciprocal? Is there a cure right?

### C10. Confidentiality scope & survival
- **What:** What is confidential, obligations, survival.
- **Why:** Over-broad confidentiality can gag disclosure of wrongdoing or legitimate use.
- **Risk vectors:** definition breadth, term length, permitted-disclosure carve-outs, return/destruction, whistleblower carve-out.
- **Red flags:** perpetual confidentiality with no carve-outs; definition capturing public info; no whistleblower exception.
- **Review questions:** Is the definition reasonable? Is there a whistleblower/legal-process exception? Is survival bounded?

### C11. Boilerplate with teeth (assignment, waiver, severability, entire-agreement, force majeure)
- **What:** Standard clauses that can hide material effects.
- **Why:** Assignment of contract, waiver, severability, integration, and force majeure materially affect rights.
- **Risk vectors:** unilateral assignment right, no-oral-modification, integration clause dropping prior promises, severability saving unfair terms, narrow/broad force majeure, notice/address-for-notice.
- **Red flags:** one party may assign freely while other cannot; force majeure too broad (includes self-caused); severability that defeats user protection.
- **Review questions:** Can the deal be assigned to a party the user did not choose? Are prior representations preserved? Is force majeure balanced?

### C12. Governing law, jurisdiction & jurisdiction-specific overlay
- **What:** Which law/forum governs.
- **Why:** Same clause can be standard in one jurisdiction and disallowed in another.
- **Risk vectors:** choice of law vs forum, mandatory venue, arbitration seat, language of proceedings.
- **Red flags:** forum distant from user; law of a jurisdiction with weaker user protections.
- **Review questions:** Is the law/forum accessible to the user? Does it disadvantage them vs home law?

---

## 3. Risk Rating Scale & Scoring

### 3.1 Rating definitions (role-relative)
| Rating | Definition |
|--------|------------|
| Critical | Materially harmful to the user; likely to cause significant loss or lock-in; or clause pattern widely disfavored/unenforceable-against-user in many jurisdictions (presented as a *consideration*, not a ruling). |
| High | Significantly one-sided; meaningful adverse impact; should be negotiated before signing. |
| Medium | Some imbalance or ambiguity; worth clarifying/negotiating. |
| Low | Minor concern; standard but worth noting. |
| Info | Neutral/standard; informational only. |

### 3.2 Scoring dimensions (overall contract risk)
| Dimension | Weight | Anchor framework |
|-----------|--------|------------------|
| Liability / indemnity balance | 25% | Risk-allocation |
| Termination / exit fairness | 20% | Contract norms |
| Restrictive covenants reasonableness | 20% | Non-compete factors |
| Hidden traps (auto-renewal / fees / unilateral change) | 20% | Consumer-protection norms |
| Clarity & completeness | 15% | ABA drafting |

Overall risk band: weighted average mapped to Low (<2.0), Medium (2.0-3.0), High (3.1-4.0), Critical (>4.0) on a 1-5 scale per dimension.

### 3.3 Per-clause rating decision aid
- One-sided risk shift with no reciprocity + material harm + disfavored pattern -> Critical.
- One-sided + material but negotiable/reasonable in context -> High.
- Ambiguity or mild imbalance -> Medium.
- Standard, minor -> Low.
- Neutral boilerplate -> Info.

---

## 4. Jurisdiction Notes (general patterns - NOT rulings)

Enforceability varies widely. These are *patterns to investigate*, never conclusions. Always tag jurisdiction and recommend local counsel.

- **Non-compete:** Some jurisdictions ban or sharply limit non-competes for many workers (e.g., California generally disallows employee non-competes; FTC rule developments and state-level reforms are ongoing - verify currency). Reasonableness factors apply elsewhere.
- **Arbitration/class waivers:** Enforceability of class-action waivers governed by federal/state arbitration law and unconscionability doctrine; varies.
- **Tenant protections:** Jurisdictions differ on security-deposit limits, notice periods, habitability warranties, auto-renewal/evergreen regulation.
- **Consumer/employment protections:** Wage, fee, and disclosure rules vary; some require plain-language summaries or specific notices.
- **Foreign-law contracts:** If the brain lacks coverage, flag limitation explicitly; provide only general risk patterns; strong local-counsel referral.

---

## 5. Role-Relative Risk Adjustment

Risk is judged from the user stated party role:
- **Employee:** restrictive covenants, at-will/termination, IP assignment, non-solicit, dispute resolution.
- **Employer:** IP assignment scope, confidentiality survival, indemnity from employee, non-compete enforceability risk, notice obligations.
- **Tenant:** auto-renewal, fees/deposits, termination/notice, repair/habitability, unilateral amendment.
- **Landlord:** default/remedies, repair obligations, indemnity, rent escalation, assignment/subletting.
- **Partner (founder):** control/voting, exit/buyout, valuation, indemnity, IP, deadlock, dispute resolution.
- **Other:** default to a balanced two-party risk-allocation view; ask for role clarification.

---

## 6. Key Research / Sources (seed; auto-grown)

| Title | Source | Year | Link | Relevance |
|-------|--------|------|------|-----------|
| Non-compete enforceability survey | SSRN | 2023 | ssrn.com | Jurisdiction variance |
| Boilerplate & consumer contracts | SSRN | 2022 | ssrn.com | Hidden-term risk |
| ABA contract drafting guidance | ABA | - | americanbar.org | Drafting principles |
| Cornell LII - contracts glossary | Cornell LII | - | law.cornell.edu/wex | Definitions & doctrine |

### Authoritative Data Sources
SSRN (ssrn.com) - scholarship; ABA (americanbar.org) - practitioner guidance; Cornell LII (law.cornell.edu) - definitions/wex; government statute portals; jurisdiction labor/tenancy summaries; FTC/CFPB for consumer-protection trends.

---

## 7. Self-Update Protocol

- **Queries:** "non-compete enforceability 2026", "contract clause risk", "tenancy law update", "arbitration clause ruling", "indemnity clause trend", "auto-renewal regulation".
- **Sources:** SSRN, ABA, Cornell LII, government portals. **Frequency:** weekly. **Tag:** jurisdiction.
- **Append format:** `- [DATE] [Jurisdiction] Title - Source - finding - URL <!--h:hash-->`. **Dedupe:** by 12-char SHA-1 hash of url+title.
- **Scoring:** recency + keyword relevance; top-N appended.
- **Safety:** never inject definitive enforceability conclusions; auto-entries are patterns/findings only.

---

## 8. Knowledge Update Log
- [2026-06-18] Seed entry - clause categories + frameworks documented.
- [2026-06-30] Deepened knowledge base: expanded 12 clause categories, scoring rubric, jurisdiction notes, role-relative adjustment, frameworks.