---
# Core Classification
protocol: generic
chain: generic
category: l1
vulnerability_type: l1_math_generic
root_cause_family: see pattern_key

# Pattern Identity
pattern_key: l1-math-generic | l1 math generic | varies by finding | see references

# Interaction Scope
interaction_scope: varies
involved_contracts:
  - l1 math generic

# Attack Vector Details
attack_type: varies
affected_component: l1 math generic

# Technical Primitives
primitives:
  - adjusted
  - block
  - calcmaxtransferrable
  - cannot
  - category
  - check

# Grep / Hunt-Card Seeds
code_keywords:
  - adjusted
  - block
  - calcmaxtransferrable
  - cannot
  - category
  - check
  - closing
  - codingmistakes

severity: critical
impact: varies
language: varies
tags:
  - generic
  - l1
  - audit-mined
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [o1] | reports/other-l1_findings/publications-audit-reports-peckshield-audit-report-boringdao-1-0-2020-89-pdf.md | CRITICAL | PeckShield | Underflows • Description: Whether the contract has general overflow or underflow vulnerabilities [8  9  10  11  13]. • Result: Not found • |
| [o2] | reports/other-l1_findings/publications-pancakeswap-aptos-zellic-audit-report-pdf.md | HIGH | Zellic | DetailedFindings 3.1 Precisionfactorisnotpreciseenough • Target:pancake::smart_chef • Category:CodingMistakes • Likelihood:High • |
| [o3] | reports/other-l1_findings/publications-reviews-2023-12-offchain-labs-arbitrum-token-bridge-creator-securityreview-pdf.md | MEDIUM | Trail of Bits | Token values in DeployHelper are not adjusted to token decimals |
| [o4] | reports/other-l1_findings/publicreports-algorand-smart-contract-audit-yieldly-finance-multi-staking-algorand-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | MISSING INTEGER UNDERFLOW PROTECTION |
| [o5] | reports/other-l1_findings/publicreports-solana-program-audit-cropper-finance-farm-solana-program-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | INTEGER OVERFLOW |
| [o6] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-axion-network-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | LACK OF INTEGER OVERFLOW PROTECTION |
| [o7] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-biconomy-vesting-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | INTEGER OVERFLOW |
| [o8] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-chiliz-bridge-updates-smart-contract-security-audit-report-halborn-final-pdf.md | CRITICAL | Halborn | INTEGER UNDERFLOW IN THE DEPOSIT FUNCTION |
| [o9] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-debt-dao-p2p-loan-smart-contract-security-audit-report-halborn-final-pdf.md | CRITICAL | Halborn | DEBT PAY OFF IMPOSSIBLE DUE TO INTEGER UNDERFLOW |
| [o10] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-gammaswap-labs-core-strategies-and-periphery-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | FIRST LIQUIDITY PROVIDER LOSES FUNDS DUE TO ROUNDING ISSUE |
| [o11] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-globedx-smart-contract-audit-halborn-v1-1-pdf.md | MEDIUM | Halborn | LACK OF OVERFLOW PROTECTION |
| [o12] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-monox-smart-contract-security-audit-report-halborn-v1-1-pdf.md | MEDIUM | Halborn | INTEGER OVERFLOW |
| [o13] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-neworderdao-smart-contract-security-audit-report-halborn-final-pdf.md | CRITICAL | Halborn | OVERFLOW IN CALCMAXTRANSFERRABLE FUNCTION |
| [o14] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-opal-finance-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | GETUSDPRICE INCORRECTLY HANDLES TOKEN DECIMALS |
| [o15] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-opal-finance-protocol-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | OPALLPTOKEN DECIMALS ARE NOT SET CORRECTLY |
| [o16] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-pangolin-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | LACK OF INTEGER OVERFLOW/UNDERFLOW PROTECTION |
| [o17] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-polemos-lending-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | VALID SIGNATURE CAN BE REJECTED DUE TO INTEGER UNDERFLOW |
| [o18] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-renzo-protocol-evm-contracts-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | INCONSISTENT DECIMAL HANDLING IN ORACLE VALUE LOOKUP |
| [o19] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-seascape-block-lords-smart-contract-security-audit-report-halborn-final-pdf.md | MEDIUM | Halborn | INTEGER OVERFLOW |
| [o20] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-seascape-zombiefarm-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | MISSING TOKEN DECIMALS CHECK |
| [o21] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-unlimited-network-unlimited-leverage-smart-contract-security-audit-report-halborn-final-pdf.md | HIGH | Halborn | PRECISION LOSS IN PARTIALLYCLOSEPOSITION FUNCTION WILL BLOCK THE LAST USER FROM CLOSING THE POSITION |
| [o22] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-wolfystreetbets-smart-contract-security-audit-report-halborn-v1-1-pdf.md | MEDIUM | Halborn | INTEGER OVERFLOW |
| [o23] | reports/other-l1_findings/publicreports-soroban-smart-contract-audits-shift-markets-cables-dex-soroban-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | LACK OF OVERFLOW CONTROL |
| [o24] | reports/other-l1_findings/publicreports-web-pentest-debridge-solana-tx-parser-whitebox-pentest-report-halborn-final-pdf.md | MEDIUM | Halborn | TRUNCATED LOGS CANNOT BE PARSED |
| [o25] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-moonwell-finance-contracts-v2-smart-contract-security-assessment-report-halborn-final-pdf.md | MEDIUM | Halborn | LACK OF END TIME VALIDATION LEADS TO WRONG MARKET INDEX CALCULATION ON THE NEW MARKETS |
| [o26] | reports/other-l1_findings/publicreports-solidity-smart-contract-audits-substance-exchange-exchange-v4-smart-contract-security-assessment-report-halborn-final-pdf.md | CRITICAL | Halborn | INCONSISTENCY IN USER BALANCE CALCULATIONS ALLOWS FOR EXPLOITS IN WITHDRAWALS |

## L1 Math Generic

**l1-math-generic patterns mined from uncited L1 audit reports** - 24 sec-tier findings (6 critical / 4 high / 14 medium) across 23 files from Halborn, PeckShield, Trail of Bits, Zellic.

### Overview

Titles in the references table are verbatim from source reports. Route to the exact report file for full PoC detail. Validation strength: `unassessed` (evidence rows only).

### Detection Patterns

#### High-Signal Grep Seeds
```
- adjusted
- block
- calcmaxtransferrable
- cannot
- category
- check
- closing
- codingmistakes
```

### Vulnerability Description

#### Root Cause

The cited reports describe l1 math generic paths where a validation, bound, or state-consistency check is missing around attacker-influenced input or an attacker-growable collection. The pattern key for this family is `l1-math-generic | l1 math generic | varies by finding | see references`. Every reference row in the table above is a verbatim finding title from the named auditor; consult that report for the exact code location and exploit path.

#### Attack Scenario / Path Variants

**Path A: [Direct input path]**
Path key: `l1-math-generic | l1 math generic | varies by finding | see references | user/peer message | direct handler`
1. Attacker submits crafted input (message, tx, packet, or config change) accepted by the entry surface.
2. Missing validation lets the input reach state mutation or an unbounded loop.
3. State corruption, fund misaccounting, or resource exhaustion follows.

**Path B: [Growth-then-trigger path]**
Path key: `l1-math-generic | l1 math generic | varies by finding | see references | cheap state growth | later iteration/execution`
1. Attacker cheaply grows a collection (plans, stakes, peers, entries).
2. A later block-time or cleanup path iterates the collection without bounds.
3. Block production exceeds limits or the node exhausts memory (DoS / halt).

### Vulnerable Pattern Examples

**Example 1: Underflows • Description: Whether the contract has general overflow or underflow vulnerabilities [8 9 10 11 13]. • Resul** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Underflows • Description: Whether the contract has general overflow or underflow vulnerabilities [8 9 10 11 13]. • Result: Not found •
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Underflows • Description: Whether the contract has general overflow or underflow vulnerabilities [8 
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 2: INTEGER UNDERFLOW IN THE DEPOSIT FUNCTION** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// INTEGER UNDERFLOW IN THE DEPOSIT FUNCTION
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: INTEGER UNDERFLOW IN THE DEPOSIT FUNCTION
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 3: DEBT PAY OFF IMPOSSIBLE DUE TO INTEGER UNDERFLOW** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// DEBT PAY OFF IMPOSSIBLE DUE TO INTEGER UNDERFLOW
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: DEBT PAY OFF IMPOSSIBLE DUE TO INTEGER UNDERFLOW
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```

### Impact Analysis

#### Technical Impact
- Wrong accounting / reward misallocation / stuck or double-counted funds (fund-loss class rows above)
- State inconsistency after partial failure (see error-handling references)
- Chain halt or node crash from unbounded work (see DoS rows)

#### Business Impact
- User fund loss and withdrawal freezes; validator downtime; consensus/partition risk for client-level bugs.

### Secure Implementation

**Fix 1: [Bound and validate at the entry surface]**
```rust
// ✅ SECURE: explicit bounds + validation before state mutation
fn handler(input: UntrustedInput) -> Result<(), Error> {
    ensure!(input.len() <= T::MaxInput::get(), Error::TooLarge);
    ensure!(is_valid(&input), Error::Invalid);
    state.update_checked(&input)?;
    Ok(())
}
```

**Fix 2: [Aggregate instead of iterate; cap growth]**
```rust
// ✅ SECURE: keep block-time work O(1) and cap attacker growth
fn on_block_end() {
    let aggregate = Aggregates::get();          // maintained incrementally
    distribute(&aggregate);                      // no unbounded iteration
}
fn create_plan(p: Plan) -> Result<(), Error> {
    ensure!(PlansCount::get() < T::MaxPlans::get(), Error::TooManyPlans);
    Ok(())
}
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- Entry surface writes state before validating attacker-controlled fields
- Block-time hooks iterate collections whose size is attacker-influenceable
- Multi-step handlers where a mid-step failure leaves earlier writes committed
- Config setters without role checks or bounds
```

#### Audit Checklist
- [ ] Verify every attacker-reachable input is length/bounds-checked before state writes
- [ ] Verify block-time (end-blocker / on_finalize) iteration is O(1) or capped
- [ ] Verify failure paths roll back partial state mutations
- [ ] Cross-check the cited reports' fix status before re-reporting

### Keywords for Search

`adjusted, block, calcmaxtransferrable, cannot, category, check, closing, codingmistakes, contract, control`

### Related Vulnerabilities

- Sibling entries under the same category folder
