---
# Core Classification
protocol: Creditswap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37110
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-12-22-CreditSwap.md
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
  - Zokyo
---

## Vulnerability Title

Missing sanity checks in `RewardAuctionHouse`

### Overview

See description below for full details.

### Original Finding Content

**Severity**: Low

**Status**:  Resolved

**Description**

There is Missing sanity checks for parameters in initialize() function. Here the minimumBid can be accidentally set to zero, or the auctionDuration can be zero as well as the beneficiary be set to zero address. This could lead to issues as these parameters can not be reset.
```solidity
        minimumBid = minimumBid_;
        auctionDuration = auctionDuration_;
        beneficiary = beneficiary_;
```

**Recommendation**: 

It is advised to add sufficient sanity checks for the above parameters.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Creditswap |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-12-22-CreditSwap.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

