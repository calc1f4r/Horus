---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41253
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#31-missing-nonce-increment-in-_updaterefundvalidatorskeyscount-function
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
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Missing Nonce Increment in `_updateRefundValidatorsKeysCount` Function

### Overview

See description below for full details.

### Original Finding Content

##### Description
The issue is identified within the [\_updateRefundValidatorsKeysCount](https://github.com/lidofinance/core/blob/fafa232a7b3522fdee5600c345b5186b4bcb7ada/contracts/0.4.24/nos/NodeOperatorsRegistry.sol#L744-L766) function of the contract `NodeOperatorsRegistry`. The current implementation lacks a call to the `_increaseValidatorsKeysNonce()` function when the `REFUNDED_VALIDATORS_COUNT_OFFSET` variable is modified. This is particularly important because the `REFUNDED_VALIDATORS_COUNT_OFFSET` variable can decrease, and failing to update the nonce could lead to discrepancies in the contract’s state, affecting other functionalities that depend on accurate nonce tracking of depositable validators' updates.

The issue is classified as **Low** severity because it could result in inconsistencies in the contract's state, potentially affecting the integrity of validator key management and related operations.

##### Recommendation
We recommend adding a call to the `_increaseValidatorsKeysNonce()` function after updating the `REFUNDED_VALIDATORS_COUNT_OFFSET` variable to ensure that all state changes are properly tracked and the nonce remains consistent.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#31-missing-nonce-increment-in-_updaterefundvalidatorskeyscount-function
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

