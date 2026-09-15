---
# Core Classification
protocol: Corgi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35356
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-28-CORGI.md
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
  - Zokyo
---

## Vulnerability Title

Missing sanity checks and division by Zero Error

### Overview


The reported bug is in the CORGI contract and it has a medium severity level. The status of the bug is acknowledged, which means it has been recognized by the developers. The bug is related to missing sanity checks for certain values in the contract. These values, called `txFee`, `burnFee`, and `FeeAddress`, can be set to any value, even above 100, which can cause problems. The same checks are also missing in the `updateFee()` function. If any of these values are set to a number greater than 100, it can lead to a division by zero error. To fix this, the report recommends adding sanity checks to ensure these values cannot be set above 100 in both the constructor and the `updateFee()` function. It also suggests adding a check to make sure `FeeAddress` is not set to a zero address in the constructor. 

### Original Finding Content

**Severity**: Medium

**Status**: Acknowledged

**Description**

In contract CORGI, there are missing sanity checks for `txFee`, `burnFee` and `FeeAddress`.
The `txFee` and `burnFee` can be arbitrarily set to any value, including value above 100. The same sanity checks are also missing in the `updateFee()` function. 
```solidity
        txFee = _txFee;
        burnFee = _burnFee;
        FeeAddress = _FeeAddress;
```
If any of `txFee` or `burnFee` is set to a value greater than 100, then it can lead to division by Zero Safemath error.
```solidity
Line: 421              uint256 DenverDeflaionaryDecay = tempValue.div(uint256(100 / txFee));
Line: 428              uint256 Burnvalue = tempValue.div(uint256(100 / burnFee));
```
Additionally, there is missing zero address check for `FeeAddress`.

**Recommendation: Add a sanity checks as follows**:

Add sanity checks to ensure that txFee & burnFee cannot be greater than 100 in both the constructor` and the `updateFee()` function.
Add a non-zero address check for `FeeAddress` in the constructor.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Corgi |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-28-CORGI.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

