# Audit Report Template

> **Purpose**: Defines the structure of the final `AUDIT-REPORT.md` produced by the `audit-orchestrator`. This is the deliverable the user receives.

---

## Report Structure

```markdown
# Security Audit Report

**Target**: [Protocol Name / Repository]
**Date**: [YYYY-MM-DD]
**Auditor**: AI-Assisted Audit (audit-orchestrator)
**Scope**: [N files, ~N LOC]
**Protocol Type**: [lending_protocol, dex_amm, etc.]

---

## Executive Summary

**Risk Level**: CRITICAL | HIGH | MODERATE | LOW

| Severity | Count |
|----------|-------|
| Critical | N |
| High | N |
| Medium | N |
| Low | N |
| Informational | N |
| **Total** | **N** |

[2-3 sentence summary of the most significant findings and overall security posture.]

### Key Risks
1. [Most critical finding — one line]
2. [Second most critical — one line]
3. [Third — one line]

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

### Methodology
1. **Automated reconnaissance** — protocol type detection, scope definition
2. **Deep context building** — line-by-line analysis of all in-scope contracts
3. **Invariant extraction** — systematic property identification
4. **DB-powered vulnerability hunting** — pattern matching against 537+ known vulnerability patterns
5. **Validation gap analysis** — input validation, access control, oracle hygiene checks
6. **Triage & PoC generation** — deduplication, falsification, exploit proof
7. **Downstream verification** — fuzzing harness generation, formal verification specs
8. **Dual severity validation** — Sherlock + Cantina criteria cross-check

---

## Findings

### Critical Findings

#### [F-001] [Title]

| Field | Value |
|-------|-------|
| **Severity** | CRITICAL |
| **Confidence** | HIGH / MEDIUM |
| **Impact** | [Concrete: "$X stolen", "total fund loss", etc.] |
| **Likelihood** | [HIGH / MEDIUM / LOW] |
| **Affected Code** | `file.ext` L123-L145 |
| **DB Pattern** | `pattern-id` (or "Novel") |
| **Sherlock** | HIGH |
| **Cantina** | CRITICAL (Impact: High, Likelihood: High) |

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

**PoC**: See `audit-output/pocs/F-001-poc.{ext}`

---

(Repeat for each finding, grouped by severity: Critical → High → Medium → Low → Informational)

### High Findings
...

### Medium Findings
...

### Low Findings
...

### Informational
...

---

## Invariant Specifications

Summary of extracted invariants that can be used for ongoing testing:

| ID | Category | Property | Scope | Testable |
|----|----------|----------|-------|----------|
| INV-S-001 | Solvency | totalDeposits >= totalBorrowed | Pool module | YES |
| INV-AC-001 | Access Control | Only admin can pause | Pool module | YES |
| ... | ... | ... | ... | ... |

Full specs: See `audit-output/02-invariants.md`

---

## Fuzzing Campaign

| Harness | Invariants Tested | Status |
|---------|-------------------|--------|
| `FuzzPool` | INV-S-001, INV-A-001 | Generated |
| ... | ... | ... |

Configuration: See `audit-output/fuzzing/medusa.json`
Harnesses: See `audit-output/fuzzing/`

---

## Formal Verification

| Spec | Properties Verified | Status |
|------|---------------------|--------|
| `Pool.spec` | INV-S-001, INV-AC-001 | Generated |
| ... | ... | ... |

Specs: See `audit-output/certora/`

---

## Severity Validation

### Sherlock Assessment
| Finding | Agent | Sherlock | Delta | Rationale |
|---------|-------|---------|-------|-----------|
| F-001 | CRITICAL | HIGH | ↓ | Sherlock caps at HIGH for this class |
| ... | ... | ... | ... | ... |

### Cantina Assessment
| Finding | Agent | Cantina | Impact | Likelihood | Rationale |
|---------|-------|---------|--------|------------|-----------|
| F-001 | CRITICAL | CRITICAL | High | High | Direct fund theft |
| ... | ... | ... | ... | ... | ... |

### Reconciled Severity
When Sherlock and Cantina disagree, **use the LOWER rating** (conservative approach):

| Finding | Sherlock | Cantina | Final | Reason |
|---------|---------|---------|-------|--------|
| F-001 | HIGH | CRITICAL | HIGH | Conservative: Sherlock is lower |

---

## Appendix

### A. Architecture Notes
[Key architectural observations from context-building phase]

### B. Assumption Register
[All assumptions documented during analysis, with confidence levels]

### C. Files Not Reviewed
[Any files excluded from scope and why]

### D. Limitations
- AI-assisted analysis may miss novel vulnerability classes not in the DB
- PoCs are generated but not fork-tested against live deployments
- Formal verification specs are syntactically generated but not proven
- Fuzzing harnesses need to be run with actual fuzzer for results
```

---

## Severity Reconciliation Rules

When Sherlock and Cantina produce different severities:

| Scenario | Rule | Final Severity |
|----------|------|----------------|
| Both agree | Use agreed severity | As-is |
| One step apart (H vs C) | Use LOWER | HIGH |
| Two steps apart (M vs C) | Use LOWER + flag for manual review | MEDIUM (flagged) |
| One says INVALID | Include finding but mark as "Disputed" | DISPUTED |
| Both say INVALID | Exclude from final report | Excluded |

---

## Quality Checklist

Before assembling the final report, verify:

- [ ] Every finding has all fields filled (severity, confidence, root cause, impact, affected code)
- [ ] CRITICAL and HIGH findings have PoC references
- [ ] Sherlock + Cantina validation completed for all findings
- [ ] Severity reconciliation applied for disagreements
- [ ] Executive summary statistics match actual finding counts
- [ ] No hallucinated file paths — every path verified via read_file
- [ ] No hallucinated line numbers — every line range verified
- [ ] DB pattern references valid (manifest ID exists)
- [ ] Invariant table matches `02-invariants.md`
- [ ] Fuzzing and Certora sections reflect actual generated files
