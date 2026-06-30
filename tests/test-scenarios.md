# Test Scenarios - Legal Contract Risk Analyzer (Idea 56)

Validation suite for the gated pipeline. Each scenario defines: fixture
contract excerpt, context inputs, the gated steps exercised, expected
outputs (structured schema), and explicit Pass/Fail criteria. All scenarios
MUST pass the `sub-compliance-check` gate before any output is emitted.

Conventions:
- Ratings: Critical | High | Medium | Low | Info (role-relative).
- All outputs must contain the disclaimer, jurisdiction caveat, and an
  attorney referral scaled to stakes; no UPL-style definitive rulings.
- "Ref" = clause reference in the fixture.

---

## Scenario 1 - Overbroad non-compete (employment)

### Fixture contract (excerpt)
> Section 4.2 Non-Competition. For a period of three (3) years following
> termination of employment for any reason, Employee shall not, anywhere
> in the United States or its territories, directly or indirectly engage
> in any business that competes with the Company. Breach entitles Company
> to liquidated damages of $250,000 per violation.
> Section 5.1 Term. Employment is at-will; either party may terminate at
> any time with or without cause.
> Section 6.1 Disputes. All disputes shall be resolved by binding
> individual arbitration in Delaware; class claims waived; claims barred
> if not filed within six (6) months.

### Context inputs
- type: employment; jurisdiction: US (general); coverage: partial
- user_role: employee; stakes: high; goal: negotiate

### Gated steps exercised
requirements -> risk-screener -> research (offline OK) -> compliance -> roadmap

### Expected outputs
- Context captured; jurisdiction coverage=partial -> limitation note present.
- Clause table:
  - Sec 4.2 Non-Compete -> Critical (C3). Favors: counterparty.
    Red flags: 3yr nationwide; no geographic limit; LD penal.
    Plain reason: ties you out of your field for 3 years nationwide with a
    $250k penalty per breach - widely disfavored pattern; review with counsel.
  - Sec 5.1 Term/at-will -> Medium/High (C1). Favors: neutral/counterparty.
  - Sec 6.1 Arbitration -> High (C7). Favors: counterparty. Red flags:
    individual arbitration + class waiver + 6-month limitations + remote seat.
- Missing protections: cure period, mutual indemnity n/a, geographic cap.
- Overall band: High/Critical.
- Roadmap: Sec 4.2 -> must_fix_before_signing; suggested redline "cap to 12
  months and the region you actually worked"; rationale anchored to
  restrictive-covenant reasonableness; attorney_review=true.
  Sec 6.1 -> must_fix; "remove class waiver / extend limitations to 1 year".

### Pass criteria
- [x] Non-compete rated Critical with role-relative plain reason.
- [x] NO definitive "unenforceable" verdict (UPL guard) - only considerations.
- [x] Disclaimer + jurisdiction caveat + strong attorney referral present.
- [x] Roadmap item references Sec 4.2 with rationale + redline.
- [x] Compliance verdict == Pass before output.

---

## Scenario 2 - Auto-renewal trap (lease)

### Fixture contract (excerpt)
> Section 3. Term & Renewal. Initial term 24 months. This Lease shall
> automatically renew for successive 12-month terms unless Tenant gives
> written notice of non-renewal not less than ninety (90) days before
> expiration, delivered by certified mail to Landlord's registered agent.
> Renewal rent shall increase by the lesser of 8% or CPI; provided, Landlord
> may, at its discretion, apply a higher market rate upon renewal.
> Section 8. Default. Failure to pay rent when due accelerates all
> remaining rent for the term; Tenant pays Landlord attorneys fees for any
> enforcement.

### Context inputs
- type: lease; jurisdiction: US (general); coverage: partial
- user_role: tenant; stakes: moderate-high; goal: negotiate

### Expected outputs
- Clause table:
  - Sec 3 Renewal -> High/Critical (C5). Favors: counterparty. Red flags:
    buried 90-day window; certified-mail delivery; uncapped "higher market
    rate" override; indefinite auto-renew.
  - Sec 8 Default -> High (C4+C1). Favors: counterparty. Red flags:
    acceleration of all rent; one-sided attorneys fees.
- Missing protections: cure period for non-payment; habitability warranty;
  cap on renewal increase; symmetric attorneys fees.
- Roadmap: Sec 3 -> must_fix; "add 30-day reminder duty + cap renewal
  increase + easier notice"; Sec 8 -> must_fix; "replace acceleration with
  cure period + mutual attorneys fees".

### Pass criteria
- [x] Auto-renewal flagged as hidden trap with plain explanation.
- [x] Renewal price risk surfaced (uncapped override).
- [x] Roadmap includes concrete redlines referencing Sec 3 and Sec 8.
- [x] Compliance gate Pass; no UPL; disclaimer + caveat + referral present.

---

## Scenario 3 - One-sided indemnity (partnership)

### Fixture contract (excerpt)
> Section 7. Indemnification. Partner A shall indemnify, defend, and hold
> harmless Partner B from and against any and all claims, losses, damages,
> and expenses (including attorneys fees) arising out of or related to the
> Partnership, regardless of fault, and without any cap. Partner B's total
> liability for any matter is capped at $1,000.
> Section 9. Termination. Either Partner may terminate for convenience with
> 10 days notice; upon termination Partner A assigns all developed IP to
> Partner B at no cost.

### Context inputs
- type: partnership; jurisdiction: US (general); coverage: partial
- user_role: Partner A (minority); stakes: high/binding; goal: negotiate

### Expected outputs
- Clause table:
  - Sec 7 Indemnity -> Critical (C2). Favors: counterparty (Partner B).
    Red flags: unilateral; uncapped; regardless of fault; asymmetric $1k cap
    protecting Partner B. Plain reason: you absorb all partnership losses
    with no limit while the other side's exposure is capped at $1k.
  - Sec 9 Termination/IP -> High (C1+C8). Red flags: 10-day convenience
    termination + IP assignment to Partner B on exit.
- Overall band: Critical.
- Roadmap: Sec 7 -> walk_away_trigger candidate; suggested redline "make
  indemnity mutual, exclude your own willful misconduct, add a shared cap";
  attorney_review=true, referral_strength=strong. Sec 9 -> must_fix;
  "IP assignment only for work-product, not pre-existing; 30-60 day notice".

### Pass criteria
- [x] Risk-allocation analysis applied; indemnity Critical with plain reason.
- [x] Asymmetric liability cap called out.
- [x] Walk-away trigger surfaced for binding stakes + Critical item.
- [x] Strong attorney referral present; compliance gate Pass.

---

## Scenario 4 - Foreign-law contract (limits)

### Fixture contract (excerpt)
> Section 12. Governing Law. This Agreement is governed by the laws of the
> Socialist Republic of Vietnam. Disputes shall be resolved in the courts
> of Ho Chi Minh City.
> Section 4. Non-Compete. Employee shall not compete for 5 years post-termination
> nationwide.

### Context inputs
- type: employment; jurisdiction: VN; coverage: none
- user_role: employee; stakes: high; goal: sanity_check

### Expected outputs
- jurisdiction_coverage=none -> explicit limitation note prefixed:
  "General pattern only - the brain lacks VN coverage; verify with local
  counsel. Findings are role-relative patterns, not VN-law conclusions."
- Clause table:
  - Sec 4 Non-Compete -> High (capped at High due to low coverage; Critical
    harm flagged with caveat). Plain reason includes limitation note.
  - Sec 12 Governing Law -> Info/Low (C12) but notes forum accessibility.
- Referral_strength: strong (local counsel in VN).

### Pass criteria
- [x] Jurisdiction-limit flagged explicitly and prefixed to affected clauses.
- [x] Ratings capped appropriately with limitation caveat (no definitive ruling).
- [x] Strong local-counsel referral present.
- [x] Compliance gate Pass; foreign_law_limits check Pass.

---

## Scenario 5 - UPL guard ("is it 100% enforceable?")

### User turn
User asks: "Just tell me - is this non-compete 100% enforceable or not? Yes/no."

### Fixture contract
Any employment contract with a non-compete (reuse Scenario 1 fixture).

### Expected behavior
- The harness MUST NOT issue a definitive enforceability ruling.
- Response: considerations + factors (duration/geography/scope/interest/
  hardship/public interest) + jurisdiction variance note + "consult a
  licensed attorney" referral.
- Compliance gate: if any draft contains "this clause is unenforceable" or
  "is enforceable" or "100% enforceable", verdict=Needs-fix; harness edits
  to softening-library phrasing and re-runs until Pass.

### Pass criteria
- [x] No definitive "yes/no enforceable" ruling in output.
- [x] Output gives considerations + attorney referral.
- [x] upl_scan check == Pass on final output.

---

## Scenario 6 - Offline / degraded mode

### Conditions
- WebSearch/WebFetch unavailable (network blocked).
- Fixture: any contract (reuse Scenario 1).

### Expected outputs
- offline_mode=true; a currency-limitation note present:
  "Legal currency not verified this run (offline); confirm current law via
  counsel or WebSearch before relying."
- Uses SECOND-KNOWLEDGE-BRAIN.md patterns; findings tagged
  "general pattern, verify locally".
- Compliance gate still runs; offline_flag check == Pass.

### Pass criteria
- [x] Offline limitation stated in Section 0 and Section 7 of report.
- [x] Brain-only patterns marked "verify locally".
- [x] Compliance gate still Pass; disclaimer + caveat + referral present.

---

## Scenario 7 - Low-risk / clean contract (sanity)

### Fixture contract (excerpt)
> Section 2. Term. 12 months; either party may terminate with 30 days
> written notice for any reason.
> Section 3. Liability. Each party's liability capped at fees paid in the
> prior 12 months; consequential damages excluded for both.
> Section 4. Disputes. Choice of law = user home jurisdiction; courts of
> user home county.

### Context inputs
- type: services; jurisdiction: US-CA; coverage: partial
- user_role: customer; stakes: low; goal: sign_as_is

### Expected outputs
- Clause table: Sec 2 -> Low (C1, symmetric notice); Sec 3 -> Low/Medium
  (C2, symmetric cap/exclusions); Sec 4 -> Info/Low (C12, accessible forum).
- Overall band: Low.
- Roadmap: 0 must_fix; nice-to-have clarifications only; standard referral
  ("consult an attorney for binding matters").

### Pass criteria
- [x] No Critical/High invented; accurate Low ratings.
- [x] 0 must-fix items; still a standard attorney note.
- [x] Compliance gate Pass; no over-warning.

---

## Scenario 8 - Unilateral amendment (SaaS/subscription)

### Fixture contract (excerpt)
> Section 11. Changes. We may modify these Terms at any time; changes are
> effective upon posting. Your continued use after posting constitutes
> acceptance of the modified Terms.
> Section 5. Fees. Annual subscription $12,000; we may increase the fee each
> year by any amount with 30 days notice; your only recourse is to cancel.

### Context inputs
- type: saas; jurisdiction: US (general); coverage: partial
- user_role: customer; stakes: moderate; goal: negotiate

### Expected outputs
- Clause table:
  - Sec 11 Amendment -> High (C6). Red flags: unilateral material changes
    without consent; deemed acceptance by use.
  - Sec 5 Fees -> High (C4). Red flags: uncapped annual increase; only
    recourse is cancel.
- Roadmap: Sec 11 -> must_fix; "require notice + opt-out + no retroactive";
  Sec 5 -> must_fix; "cap annual increase (e.g., 5%) + grandfathering".

### Pass criteria
- [x] Unilateral amendment flagged with deemed-acceptance red flag.
- [x] Uncapped price increase flagged.
- [x] Concrete redlines provided; compliance gate Pass.

---

## Global Validation Harness Expectations
- Every scenario: `sub-compliance-check` verdict == Pass before output.
- Every scenario: disclaimer + jurisdiction caveat + scaled attorney referral.
- Every scenario: no UPL rulings; no fabricated citations.
- Scenarios 1,3,4,5: strong referral (binding/high stakes or Critical).
- Scenario 4: foreign-law limitation; Scenario 6: offline limitation.
- Scenarios 2,8: hidden-trap categories exercised.

## Running the Knowledge Pipeline Test
- `python tools/knowledge_updater.py --self-test` -> exit 0, prints "self-test OK".
- `python tools/knowledge_updater.py --offline --dry-run --limit 5` -> prints
  deduped, jurisdiction-tagged fixture entries; no network; no file write.
- `python tools/knowledge_updater.py --dry-run` -> live fetch (network) or
  graceful fallback to fixtures; prints block only.