---
# Core Classification
protocol: Kuiper
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19847
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-12-defiProtocol
source_link: https://code4rena.com/reports/2021-12-defiProtocol
github_link: https://github.com/code-423n4/2021-12-defiprotocol-findings/issues/152

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

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-10] Fee calculation is slightly off

### Overview


This bug report is about a fee calculation in the Basket.sol contract on the 2021-12-defiprotocol project. The calculation tries to calculate a fee such that fee/(supply+fee) = %fee using a simple interest formula (i.e. no compounding). This leads to slightly less fee collected when fee are collected more frequently (small timeDiff) vs less frequently (big timeDiff). This precision loss issue was acknowledged by frank-beard (Kuiper) and 0xleastwood (judge) and was given a medium severity rating. The precision loss or value leakage could lead to an inconsistent fee calculation and is worth fixing.

### Original Finding Content

_Submitted by gzeon_

The fee calculation
```solidity
uint256 timeDiff = (block.timestamp - lastFee);
uint256 feePct = timeDiff * licenseFee / ONE_YEAR;
uint256 fee = startSupply * feePct / (BASE - feePct);
```
tries to calculate a fee such that fee/(supply+fee) = %fee using a simple interest formula (i.e. no compounding), this lead to slightly less fee collected when fee are collected more frequently (small timeDiff) vs less frequently (big timeDiff).

### Proof of Concept

[Basket.sol#L133](https://github.com/code-423n4/2021-12-defiprotocol/blob/205d3766044171e325df6a8bf2e79b37856eece1/contracts/contracts/Basket.sol#L133)

**[frank-beard (Kuiper) acknowledged, but disagreed with Medium severity and commented](https://github.com/code-423n4/2021-12-defiprotocol-findings/issues/152#issuecomment-1048146206):**
 > While this is technically true, the actual precision loss should be very negligible.

**[0xleastwood (judge) commented](https://github.com/code-423n4/2021-12-defiprotocol-findings/issues/152#issuecomment-1079829640):**
 > I think any precision loss or value leakage qualifies for a `medium` severity issue. This seems like it would lead to an inconsistent fee calculation and is probably worthwhile fixing long-term.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Kuiper |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-12-defiProtocol
- **GitHub**: https://github.com/code-423n4/2021-12-defiprotocol-findings/issues/152
- **Contest**: https://code4rena.com/reports/2021-12-defiProtocol

### Keywords for Search

`vulnerability`

