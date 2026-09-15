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
solodit_id: 41055
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

Missing input validation on fee parameters

### Overview

See description below for full details.

### Original Finding Content

## Risk Assessment Report

## Severity
**Low Risk**

## Context
- **File**: AxiomV2Query.sol
- **Line Numbers**: L156, L163

## Description
The functions `updateProofVerificationGas()` and `updateAxiomQueryFee()` update two "fee" parameters without enforcing any bound checks on them. Therefore, the updated values can be as extreme as `0` or `type(uint256).max`. 

This may affect user experience if a malicious or compromised user with the `TIMELOCK_ROLE` executes a fee change that front-runs some query. As a result, the user may end up spending significantly more ether to fulfill said query, or in extreme cases (if the user does not have enough funds to back up the query), this could lead to a Denial of Service (DoS) situation.

## Recommendation
Setting reasonable upper and lower bounds on these fee parameters would improve trustlessness, making it harder to create a DoS situation under the scenario of a compromised `TIMELOCK_ROLE` user front-running a query with a fee change. In fact, the documentation specifies some initial values (400000 and ...).

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

