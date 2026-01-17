---
# Core Classification
protocol: Filament
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45610
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-08-15-Filament.md
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
finders_count: 1
finders:
  - Zokyo
---

## Vulnerability Title

Interest Could Be Calculated As 0 Due To Rounding

### Overview


This bug report is about a formula used to calculate interest in the updateBalances function. The formula currently uses a fixed interval value of 1, which may cause incorrect interest calculations when the borrowing rate and borrowed amount are large. This can result in a scenario where the interest applied is rounded down to 0, resulting in no interest being applied to the index token. The recommendation is to either have a minimum interval or increase the precision of the formula to prevent this issue. The bug has been resolved.

### Original Finding Content

**Severity** - High

**Status** - Resolved

**Description**

In the updateBalances function the formula to calculate interest (short or long) is as follows →
```solidity
uint256 shortInterest = (borrowingRate * interval * s.borrowedAmountFromPool[_indexToken].short)
            / (INTERESTRATE_DECIMALS * 365 * 86_400);
```
Consider the following scenario ->

Borrow rate for the index token = 3e3

Borrow amount from pool = 1e10 (10k USD)

Since the contracts would be deployed on SEI , the block time would be < 1 , let’s assume interval to be 1 , and consider attacker is calling this via a bot every second (cheap gas on L2)

Therefore the equation becomes →

Interest = (3e3)(1)(1e10) / (1e6)(31536000) = 30000 / 31536

Which rounds down to 0  , therefore the interest that would be applied is 0 on the index token.

**Recommendation**:

Have a minimum interval or increase precision of the formula

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Filament |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-08-15-Filament.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

