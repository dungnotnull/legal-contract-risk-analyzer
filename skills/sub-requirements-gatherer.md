---
name: sub-requirements-gatherer
description: Capture contract type, governing-law jurisdiction, the user party role, goals, and constraints before analysis. BLOCKS the harness if jurisdiction or role cannot be determined.
---

## Purpose
Establish the context that determines how clauses are interpreted and rated. Risk is role-relative and jurisdiction-dependent; without context the analysis would mislead the user.

## Inputs
- Contract text (full agreement, including recitals, definitions, schedules).
- Contract type (if user states it): employment | lease | partnership | NDA | SaaS/subscription | other.
- Governing-law / jurisdiction clause (from the contract or stated by user).
- Which party the user is (employee/employer, tenant/landlord, partner, customer/vendor).
- User goals: sign as-is? negotiate? walk away? specific concerns.
- Constraints: deadlines, must-keep clauses, leverage, language.

## Process
1. **Identify contract type** from explicit title/recitals; if absent, infer from dominant subject matter and confirm with the user. Tag one of: employment, lease, partnership, NDA, SaaS/subscription, services, vendor, other.
2. **Locate governing law / jurisdiction.** Scan for "governing law", "jurisdiction", "venue", "choice of law", arbitration seat. If absent, ask the user for the jurisdiction whose law applies. If the user cannot provide it, flag jurisdiction as UNKNOWN and proceed with general patterns only (see Compliance check).
3. **Determine the user party role.** Map role to a role bucket:
   - Employment -> employee | employer
   - Lease -> tenant | landlord
   - Partnership -> partner (note majority/minority if known)
   - Other -> user-supplied role label (e.g., customer, vendor, licensee)
4. **Capture goals & constraints** in a structured record:
   - goal: { sign_as_is, negotiate, walk_away, sanity_check }
   - concerns: list of clauses the user is worried about (free text)
   - constraints: deadline, non-negotiables, leverage, language preference
   - stakes: { low, moderate, high, binding } (binding/high stakes trigger strong attorney referral downstream)
5. **Coverage check.** If jurisdiction is a foreign law not covered by SECOND-KNOWLEDGE-BRAIN.md, set `jurisdiction_coverage = partial | none` so the screener can flag limitations.
6. **Block condition.** If jurisdiction OR user role cannot be determined AND the user has not authorized a general-patterns-only run, BLOCK and request the missing item. Do not invent it.

## Output Schema (context object)
```yaml
context:
  contract_type: employment | lease | partnership | NDA | saas | services | other
  contract_title: <string or null>
  jurisdiction: <string, e.g., "US-CA", "EU", "VN", "UNKNOWN">
  jurisdiction_coverage: full | partial | none
  user_role: <string, role bucket>
  user_role_side: <string, e.g., employee/employer>
  goals:
    primary: sign_as_is | negotiate | walk_away | sanity_check
    concerns: [ <string> ]
  constraints:
    deadline: <string or null>
    non_negotiables: [ <string> ]
    leverage: <string or null>
    language: <string or null>
  stakes: low | moderate | high | binding
  offline_mode: true | false
  notes: <string>
```

## Decision Aids
- **Stakes heuristic:** employment non-compete/termination, lease >12 months with auto-renewal, partnership with equity/exit, or any indemnity uncapped -> high/binding.
- **Role inference:** if contract is one-sided drafted (form) and user is the weaker-signing party, default role to that weaker side and confirm.
- **Jurisdiction normalization:** accept free text; normalize to a tag (ISO country/region where known; else literal). Keep original text in notes.

## Quality Gate
- [ ] Jurisdiction explicitly set (or UNKNOWN with authorization for general-only run).
- [ ] User role explicitly set (or BLOCK issued).
- [ ] Stakes recorded (drives attorney-referral strength downstream).
- [ ] Jurisdiction coverage flag set.
- [ ] Concerns and constraints captured for the roadmap.

## Failure / Edge Cases
- **No governing-law clause:** treat as UNKNOWN; ask user; never assume.
- **Multiple jurisdictions / split clauses (choice of law vs forum):** record both; note divergence.
- **User asks "is this enforceable?":** do NOT answer here; route to compliance gate (UPL guard).
- **Foreign law the brain lacks:** set coverage=none; screener emits general patterns only; strong local-counsel referral.