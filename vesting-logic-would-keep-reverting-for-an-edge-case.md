---
# Core Classification
protocol: Zap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35446
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-04-11-zap.md
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

Vesting Logic Would Keep Reverting For An Edge Case

### Overview


The report states that there is a bug in the system where users are unable to claim their vested shares due to an overflow error. This is caused by a miscalculation in the contract `TokenSaleUSDB` and `TokenSaleETH.sol` which results in an incorrect normalization of the `amountFinal` when the `tokenAddress` has more than 18 decimals. This allows malicious users to create a `TokenSale` with a token that has 22 decimals, causing the system to revert and prevent users from claiming their shares. The recommendation is to restrict tokens to 18 decimals or adjust the normalization accordingly. This bug has been marked as resolved. 

### Original Finding Content

**Severity**: High

**Status**: Resolved

**description**

The normal flow in the system is , users deposit , they deposit is raised and liquidity is added
to pancakeSwap and users can vest their shares using the function `vesting()` .
In the contract `TokenSaleUSDB` (same for `TokenSaleETH.sol`) the `decimalDifference` is
calculated at L281 which is used to normalise the `amountFinal` . But if the `tokenAddress’s`
decimal is more than 18 then the calculation at L281 would always revert due to overflow.
Therefore a malicious user can create a `TokenSale` where token is a token with 22 decimals
and make the users deposit their share into the pool , but the users would never be able to
claim their vest due to the overflow error .

**Recommendation:**

Restrict token to 18 decimals or normalise accordingly.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Zap |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-04-11-zap.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

