# Audit Report Template

> **Purpose**: Defines the structure of the final `CONFIRMED-REPORT.md` produced by the `audit-orchestrator`. This is the deliverable the user receives. Only CONFIRMED findings (judge consensus + judging self-loop verification) appear in the main body. Adapts to pipeline mode (`--static-only`, `--judge=X`, `--discovery-rounds=N`).

---

## Report Structure

```markdown
# Confirmed Security Audit Report

**Target**: [Protocol Name / Repository]
**Date**: [YYYY-MM-DD]
**Auditor**: AI-Assisted Audit (audit-orchestrator — 11-phase pipeline)
**Scope**: [N files, ~N LOC]
**Protocol Type**: [lending_protocol, dex_amm, etc.]

## Pipeline Configuration
| Setting | Value |
|---------|-------|
| **Mode** | full / static-only |
| **Judge Mode** | full (Sherlock + Cantina + Code4rena) / single ([judge name]) |
| **Discovery Rounds** | N |
| **Phases Skipped** | [None / 6 (PoC), 7 (FV)] |

---

## Executive Summary

**Risk Level**: CRITICAL | HIGH | MODERATE | LOW

| Severity | Confirmed | Demoted | Disputed | Rejected |
|----------|-----------|---------|----------|----------|
| Critical | N | N | N | N |
| High | N | N | N | N |
| Medium | N | N | N | N |
| Low | N | N | N | N |
| **Total** | **N** | **N** | **N** | **N** |

[2-3 sentence summary of the most significant confirmed findings and overall security posture.]

### Key Confirmed Risks
1. [Most critical confirmed finding — one line + evidence]
2. [Second most critical — one line + evidence]
3. [Third — one line + evidence]

### Confirmation Methodology
Each finding passed a **judging self-loop**:
1. **Pre-Judging (Phase 8)**: Judge(s) screen all triaged findings for validity
2. **Issue Polishing (Phase 9)**: Valid findings polished into submission-ready write-ups
3. **Deep Review (Phase 10)**: Same judge(s) perform line-by-line verification of polished findings

**Consensus requirement**: [2-of-3 judges (full mode) / 1-of-1 judge (single-judge mode)]
**Execution evidence**: [Required (full mode) / Not required — static analysis only (static-only mode)]

---

## Scope & Methodology

### Files Audited
| File | LOC | Description |
|------|-----|-------------|
| ... | ... | ... |

### Protocol Classification
- **Detected types**: [from Phase 1]
- **DB Manifests consulted**: [list of manifests loaded]
- **Total DB patterns checked**: N

### 11-Phase Pipeline
1. **Reconnaissance** — protocol detection, scope, manifest resolution
2. **Deep context building** — line-by-line analysis (function-analyzer × N → system-synthesizer)
3. **Invariant extraction + review** — invariant-writer → invariant-reviewer
4. **Iterative parallel discovery** — N rounds of: DB hunt + reasoning + 6-persona + validation gap (with cross-pollination between rounds)
5. **Merge & triage** — cross-source correlation, deduplication, falsification
6. **PoC generation & EXECUTION** — [CONDITIONAL] PoCs compiled and run
7. **Formal verification generation & EXECUTION** — [CONDITIONAL] Medusa + Certora + Halmos run
8. **Pre-Judging** — judge(s) screen all triaged findings for validity
9. **Issue polishing** — submission-ready write-ups (valid findings only)
10. **Deep review** — same judge(s) do line-by-line verification
11. **Report assembly** — this document

---

## Confirmed Findings

### Critical Findings

#### [F-001] [Title] — CONFIRMED

| Field | Value |
|-------|-------|
| **Severity** | CRITICAL |
| **Confidence** | HIGH |
| **Impact** | [Concrete: "$X stolen", "total fund loss", etc.] |
| **Likelihood** | HIGH |
| **Affected Code** | `file.ext` L123-L145 |
| **DB Pattern** | `pattern-id` (or "Novel") |
| **Discovery Source** | Phase 4A-R1 (DB Hunt) + Phase 4C-R2 (State Machine persona) |
| **Discovery Round** | R1 (initial), confirmed variant in R2 |
| **PoC Status** | PASS ✅ (or N/A if --static-only) |
| **FV Status** | VIOLATED INV-S-001 ✅ (or N/A if --static-only) |
| **Pre-Judge (Phase 8)** | VALID ✅ |
| **Deep Review (Phase 10)** | CONFIRMED ✅ |
| **Judge(s)** | Sherlock(H), Cantina(CRIT), Code4rena(2) — or single judge name |
| **Judge Consensus** | 3/3 VALID (or 1/1 if --judge=X) |

**Root Cause**: [One sentence]

**Description**: [Detailed explanation of the vulnerability, why it exists, and what assumptions are violated.]

**Attack Scenario**:
1. Attacker calls `function()` with malicious parameters
2. This causes state X to become inconsistent
3. Attacker extracts value by calling `withdraw()`

**Vulnerable Code**:
```
// file L123-L145 (use target language)
function vulnerable() {
    // ❌ VULNERABLE: missing check
}
```

**Recommended Fix**:
```
function secure() {
    // ✅ SECURE: added validation
}
```

**Execution Evidence**:

*PoC Output* (from `audit-output/pocs/F-001-poc.{ext}`):
```
forge test --match-test test_F001_exploit -vvv
[PASS] test_F001_exploit() (gas: 245891)
Logs:
  Attacker balance before: 0
  Attacker balance after: 100000000000000000000
```

> **Static-only mode**: Omit this section entirely. Add note: "Execution evidence not generated (--static-only mode)."

*FV Violation* (from Halmos):
```
halmos --function check_INV_S_001
...
Counterexample found: ...
```

---

(Repeat for each confirmed finding, grouped by severity: Critical → High → Medium → Low)

### High Findings
...

### Medium Findings
...

### Low Findings
...

---

## Invariant Specifications

Summary of extracted and reviewed invariants:

| ID | Category | Property | Scope | Review | FV Result |
|----|----------|----------|-------|--------|-----------|
| INV-S-001 | Solvency | totalDeposits >= totalBorrowed | Pool | TIGHTENED | VIOLATED (F-001) |
| INV-AC-001 | Access Control | Only admin can pause | Pool | UNCHANGED | VERIFIED |
| ... | ... | ... | ... | ... | ... |

Full specs: See `audit-output/02-invariants-reviewed.md`

---

## Execution Evidence Summary

> **Static-only mode**: Replace this entire section with: "Phases 6-7 skipped (`--static-only`). Findings confirmed through judging self-loop only."

### PoC Results
| Finding | PoC File | Status | Notes |
|---------|----------|--------|-------|
| F-001 | pocs/F-001-poc.sol | PASS ✅ | Stole 100 ETH |
| F-002 | pocs/F-002-poc.sol | PASS ✅ | Drained pool |
| ... | ... | ... | ... |

### Formal Verification Results
| Tool | Specs | Compiled | Executed | Violations |
|------|-------|----------|----------|------------|
| Medusa | N | ✅ | ✅ | N violations |
| Certora | N | ✅ | ✅ | N violations |
| Halmos | N | ✅ | ✅ | N violations |

Violation → Finding mapping: See `audit-output/07-fv-results.md`

---

## Judging Self-Loop Summary

### Phase 8: Pre-Judge Screening
| Finding | Judge(s) | Verdict | Rationale |
|---------|----------|---------|----------|
| F-001 | [judge names] | VALID | [one-line reason] |
| F-004 | [judge names] | INVALID | [one-line reason — eliminated here] |
| ... | ... | ... | ... |

**Eliminated at pre-judge**: N findings removed before polishing.

### Phase 10: Deep Review Verification
| Finding | Judge(s) | Code Verified | Logic Verified | Verdict |
|---------|----------|--------------|---------------|---------|
| F-001 | [judge names] | ✅ | ✅ | CONFIRMED |
| F-003 | [judge names] | ✅ | ❌ | NEEDS-REVISION → DEMOTED |
| ... | ... | ... | ... | ... |

### Severity Consensus Matrix
| Finding | Sherlock | Cantina | Code4rena | Consensus | Final |
|---------|---------|---------|-----------|-----------|-------|
| F-001 | HIGH | CRITICAL | 2 (High) | 3/3 | HIGH |
| F-002 | HIGH | HIGH | 2 (High) | 3/3 | HIGH |
| ... | ... | ... | ... | ... | ... |

> **Single-judge mode**: Only one column populated. Consensus is 1/1.

### Reconciliation Rules
When judges disagree, the **minimum of the 2+ agreeing judges' severity** is used (conservative).

---

## Discovery Cross-Pollination Record

### Rounds Executed: N

| Round | New Findings | Variants Found | Cross-Checks Resolved |
|-------|-------------|----------------|----------------------|
| R1 | N | — | — |
| R2 | N | N (from R1 seeds) | N confirmed, M rejected |

### Cross-Pollination Highlights
- **R1 → R2**: [Example: "4A found oracle staleness → 4C confirmed variant in liquidation path"]
- **R2 → R3**: [Example: "4B reasoning found reentrancy → 4A searched DB for reentrancy variants"]

Full discovery state files: See `audit-output/discovery-state-round-*.md`

---

## Fuzzing Campaign

| Harness | Invariants Tested | Executed | Result |
|---------|-------------------|----------|--------|
| `FuzzPool` | INV-S-001, INV-A-001 | ✅ | 2 violations found |
| ... | ... | ... | ... |

Configuration: See `audit-output/fuzzing/medusa.json`

---

## Formal Verification Specs

| Spec | Properties | Tool | Executed | Result |
|------|-----------|------|----------|--------|
| `Pool.spec` | INV-S-001, INV-AC-001 | Certora | ✅ | 1 violation |
| `test_Pool.t.sol` | INV-S-001 | Halmos | ✅ | 1 counterexample |

Specs: See `audit-output/certora/`, `audit-output/halmos/`

---

## Pipeline Execution Record

| Phase | Duration | Status | Artifacts |
|-------|----------|--------|-----------|
| 1: Recon | — | ✅ | 00-scope.md |
| 2: Context | — | ✅ | 01-context.md + N per-contract files |
| 3: Invariants | — | ✅ | 02-invariants-reviewed.md |
| 4-R1: Discovery (Round 1) | — | ✅ | 03/04a/04c/04d findings + discovery-state-round-1.md |
| 4-R2: Discovery (Round 2) | — | ✅ | round-2 findings + discovery-state-round-2.md |
| 5: Triage | — | ✅ | 05-findings-triaged.md (N triaged) |
| 6: PoC Exec | — | ✅/SKIPPED | N PoCs, M PASS (or skipped: --static-only) |
| 7: FV Exec | — | ✅/SKIPPED | 3 tools, K violations (or skipped: --static-only) |
| 8: Pre-Judging | — | ✅ | 08-pre-judge-results.md (N valid, M invalid) |
| 9: Issue Polishing | — | ✅ | 09-polished-findings.md + issues/ |
| 10: Deep Review | — | ✅ | 10-deep-review.md (N confirmed, M demoted) |
| 11: Report | — | ✅ | This document |

Full pipeline state: See `audit-output/pipeline-state.md`

---

## Appendix

### A. Demoted Findings (Likely Valid — Unverified)
Findings where judge(s) confirmed validity but either:
- No execution evidence (static-only mode or PoC SKIP/FAIL)
- Deep review returned NEEDS-REVISION and retry also failed

(findings listed in standard format with DEMOTED tag)

### B. Disputed Findings (For Human Review)
Findings where execution evidence exists (PoC passes) but judge(s) disagreed on validity:

(findings listed with PoC evidence and judge rationales)

### C. Architecture Notes
[Key architectural observations from context-building phase]

### D. Assumption Register
[All assumptions documented during analysis, with confidence levels]

### E. Files Not Reviewed
[Any files excluded from scope and why]

### F. Limitations
- AI-assisted analysis may miss novel vulnerability classes not in the DB
- PoCs run against local test environment (not fork-tested against live deployments unless setup available)
- Formal verification counterexamples may need manual interpretation
- Judge consensus is based on automated severity criteria (Sherlock + Cantina + Code4rena rules)
- Multi-persona consensus strengthens confidence but does not guarantee correctness
```

---

## Severity Reconciliation Rules

**Full judge mode** (Sherlock + Cantina + Code4rena):

| Scenario | Rule | Final Severity |
|----------|------|----------------|
| All 3 agree | Use agreed severity | As-is |
| 2 agree, 1 differs | Use the 2-judge consensus severity | As agreed |
| All 3 differ | Use LOWEST | Conservative |
| 2+ say INVALID | Exclude from confirmed (→ REJECTED) | Excluded |
| 1 says INVALID, 2 say valid | Include as CONFIRMED with note | 2-judge severity |
| All say INVALID | Archive as REJECTED | Excluded |

**Single-judge mode** (`--judge=X`):

| Scenario | Rule | Final Severity |
|----------|------|----------------|
| Judge says valid | Use judge's severity | As-is |
| Judge says INVALID | Exclude (→ REJECTED) | Excluded |

---

## Confirmation Requirements

**Full mode** — a finding is CONFIRMED when ALL of:
1. **2-of-3 judges** rate it valid at pre-judge (Phase 8)
2. **Execution evidence** exists: PoC PASS, FV VIOLATED, or detailed reachability proof
3. **Deep review (Phase 10)** returns CONFIRMED by 2-of-3 judges
4. **Severity** is the minimum of the agreeing judges' ratings

**Static-only mode** — a finding is CONFIRMED when ALL of:
1. **2-of-3 judges** rate it valid at pre-judge
2. **Deep review** returns CONFIRMED (execution evidence NOT required)
3. **Severity** is the minimum of the agreeing judges' ratings

**Single-judge mode** — a finding is CONFIRMED when:
1. Judge rates it valid at pre-judge
2. Deep review returns CONFIRMED (1/1 consensus)

A finding is DEMOTED when:
- Judge(s) say valid BUT deep review returns NEEDS-REVISION after retry

A finding is DISPUTED when:
- PoC passes BUT judge(s) say INVALID (potential false negative from judges)

A finding is REJECTED when:
- Judge(s) say INVALID at pre-judge (Phase 8) — never polished

---

## Quality Checklist

Before assembling the final report, verify:

**Configuration**:
- [ ] Pipeline Configuration table filled in (mode, judge mode, discovery rounds)
- [ ] Skipped phases annotated correctly

**Pipeline Completeness**:
- [ ] Every confirmed finding has all fields filled (severity, confidence, root cause, impact, affected code)
- [ ] CRITICAL and HIGH findings have PoC with PASS status (unless --static-only)
- [ ] Phase 8 pre-judging completed for all findings — invalid findings eliminated
- [ ] Phase 9 issue polishing completed for valid findings only
- [ ] Phase 10 deep review completed — findings are CONFIRMED or DEMOTED
- [ ] Severity reconciliation applied for disagreements
- [ ] DEMOTED findings in Appendix A with explanations
- [ ] DISPUTED findings in Appendix B for human review

**Findings Quality**:
- [ ] Executive summary statistics match actual finding counts per category
- [ ] No hallucinated file paths — every path verified via read_file
- [ ] No hallucinated line numbers — every line range verified
- [ ] DB pattern references valid (manifest ID exists)

**Execution Evidence (full mode only)**:
- [ ] PoC results table matches `06-poc-results.md`
- [ ] FV results table matches `07-fv-results.md`
- [ ] Fuzzing and FV sections reflect actual executed results (not just generated)

**Static-Only Mode**:
- [ ] Execution Evidence sections annotated as "Skipped (--static-only)"
- [ ] No execution evidence required in confirmation criteria
- [ ] Findings confirmed through deep review only

**Judging Self-Loop**:
- [ ] Pre-judge results table complete (Phase 8)
- [ ] Deep review results table complete (Phase 10)
- [ ] NEEDS-REVISION findings retried max 1 time
- [ ] Severity consensus matrix matches actual judge outputs

**Discovery Cross-Pollination**:
- [ ] All discovery rounds reflected in pipeline execution record
- [ ] Discovery source column shows round number (e.g., 4A-R1, 4C-R2)

**Report Structure**:
- [ ] Invariant table matches `02-invariants-reviewed.md`
- [ ] Judge verdicts tables match `08-pre-judge-results.md` and `10-deep-review.md`
- [ ] Pipeline execution record accurately reflects all phases
- [ ] Appendices complete for demoted and disputed findings
