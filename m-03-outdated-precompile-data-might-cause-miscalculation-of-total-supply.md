---
# Core Classification
protocol: stHYPE_2025-10-13
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63215
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/stHYPE-security-review_2025-10-13.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-03] Outdated precompile data might cause miscalculation of total supply

### Overview


The bug report discusses an issue with the `Overseer.rebase()` function that calculates the total supply of HYPE owned by the protocol. The calculation uses different precompiles to get the balances of different addresses in the L1, but these precompiles return the state from the start of the current block. This means that if previous actions took place in the same block, the total supply might be miscalculated. This can result in a lower total supply than expected, similar to a slashing event, which can have different outcomes. The report recommends coordinating movements of HYPE by the `interimAddress` and calls to `rebase()` to avoid them happening in the same block, or reverting in `rebase()` if the contract has interacted with the staking modules in the current block. 

### Original Finding Content


_Resolved_

## Severity

**Impact:** High

**Likelihood:** Low

## Description

`Overseer.rebase()` calls the `getNewSupply()` function to determine the total supply of HYPE owned by the protocol. In this calculation, different precompiles are used to get the balances of different addresses in the L1. In this regard, it is important to note that these precompiles return the state from **the start of the current block**.

This means that if previous actions took place in the same block, the total supply might be miscalculated. These actions include the movement of HYPE from and to the L1 by the staking modules or the interim address.

As a result, the total supply can be lower than expected, similar to the occurrence of a slashing event, which will cause different outcomes, as the share price decreases and the protocol receiving extra fees once the supply is recovered.

## Recommendations

- Revert in `rebase()` if in the current block the contract has interacted with the staking modules.
- Coordinate movements of HYPE by the `interimAddress` and calls to `rebase()` to avoid them happening in the same block.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | stHYPE_2025-10-13 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/stHYPE-security-review_2025-10-13.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

