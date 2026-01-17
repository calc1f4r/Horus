---
# Core Classification
protocol: Axiom Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41054
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Axiom-contracts-Spearbit-Security-Review-October-2023.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Axiom-contracts-Spearbit-Security-Review-October-2023.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - Blockdev
  - Riley Holterhus
  - Desmond Ho
  - Lucas Goiriz
  - David Chaparro
---

## Vulnerability Title

Missing sanity zero-address checks may lead to undesired behavior

### Overview

See description below for full details.

### Original Finding Content

## Severity: Low Risk

## Context
- **Files**: 
  - AxiomV2Query.sol#L114-L131
  - AxiomV2Core.sol#L257-L270
  - AxiomV2Client.sol#L15
  - AxiomTimelock.sol#L20

## Description
Certain logic should implement zero-address checks to avoid undesired behavior.
- `verifierAddress`, `axiomHeaderVerifierAddress`, and `axiomProverAddress` implement these checks at the initializer. Nonetheless, these checks are absent in their updater functions, which leaves an open door to setting the default value `address(0)` by the TIMELOCK_ROLE Axiom multisig by mistake. This scenario could create a temporary DoS until the value is changed back to a valid one.
- For immutable variables such as `axiomV2QueryAddress`, it is recommended that these checks are included too.
- For the timelock controller, a zero `minDelay` effectively negates the purpose of having a delay, which contradicts the expected outcome. With a value of `0` or a very low number, concerns arise about administrative actions being executed without providing users sufficient time to make an informed decision about whether to continue using the system. Examples of critical actions that could be affected include `upgradeTo()` and `updatingFees()`, among others.

## Recommendation
Consider adding zero-address checks on the aforementioned variables within their updater functions, and revert with the already defined appropriate error messages.

## Axiom
- Added zero-address checks for updater functions in PR 83.
- Added zero-address check for `axiomV2QueryAddress` in PR 134.
- Minimum delay added in PR 119.

## Spearbit
Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Axiom Contracts |
| Report Date | N/A |
| Finders | Blockdev, Riley Holterhus, Desmond Ho, Lucas Goiriz, David Chaparro |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Axiom-contracts-Spearbit-Security-Review-October-2023.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Axiom-contracts-Spearbit-Security-Review-October-2023.pdf

### Keywords for Search

`vulnerability`

