---
# Core Classification
protocol: infiniFi contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55051
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/InfiniFi-Spearbit-Security-Review-March-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/InfiniFi-Spearbit-Security-Review-March-2025.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - R0bert
  - Slowfi
  - Jonatas Martins
  - Noah Marconi
---

## Vulnerability Title

Incorrect accounting in LockingController.applyLosses function

### Overview


This is a report about a bug found in the code for LockingController.sol. The bug is classified as a high risk vulnerability and is located on line 415 of the file. The issue is in the `applyLosses` function, where the code is incorrectly distributing negative `yield_amount` among each epoch bucket. This is due to a mistake in the calculation, where the denominator is being artificially decremented in each iteration of the for loop. This results in an incorrect sum of allocations and corrupts the final accounting. To fix this, the calculation should use the correct state variable instead of the incorrectly decremented one. The bug has been fixed and verified by the development team.

### Original Finding Content

## Vulnerability Report

## Severity
**High Risk**

## Context
**File:** LockingController.sol  
**Location:** Line 415

## Description
In the `applyLosses` function, the code attempts to distribute the negative `yield_amount` among each epoch bucket by computing:

```solidity
uint256 allocation = epochTotalReceiptToken.mulDivUp(_amount, _globalReceiptToken);
_globalReceiptToken -= allocation;
```

Because `_globalReceiptToken` is decremented in each iteration of the for loop, each bucket's allocation is calculated over a progressively smaller denominator. This will cause the sum of all allocations to exceed `_amount`, leading to more slash than intended. Worse, at the end of the loop, `globalReceiptToken` and `globalRewardWeight` are incorrectly set to these artificially decremented values, corrupting the final accounting.

## Recommendation
To fix this accounting error and ensure accurate loss distribution, the allocation calculation should use the state variable `globalReceiptToken` as the denominator instead of `_globalReceiptToken`. The corrected line of code should read:

```solidity
uint256 allocation = epochTotalReceiptToken.mulDivUp(_amount, globalReceiptToken);
```

## Status
**infiniFi:** Fixed in b9af8d.  
**Spearbit:** Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | infiniFi contracts |
| Report Date | N/A |
| Finders | R0bert, Slowfi, Jonatas Martins, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/InfiniFi-Spearbit-Security-Review-March-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/InfiniFi-Spearbit-Security-Review-March-2025.pdf

### Keywords for Search

`vulnerability`

